import asyncio
import logging
import serial
import serial_asyncio

from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from dsmr_parser.exceptions import ParseError
from dsmr_parser.parsers import TelegramParser, TelegramParserV2_2, \
    TelegramParserV4
from dsmr_parser.clients.settings import SERIAL_SETTINGS_V2_2, \
    SERIAL_SETTINGS_V4


logger = logging.getLogger(__name__)


class SerialReader(object):
    PORT_KEY = 'port'

    def __init__(self, device, serial_settings, telegram_specification):
        self.serial_settings = serial_settings
        self.serial_settings[self.PORT_KEY] = device

        if serial_settings is SERIAL_SETTINGS_V2_2:
            telegram_parser = TelegramParserV2_2
        elif serial_settings is SERIAL_SETTINGS_V4:
            telegram_parser = TelegramParserV4
        else:
            telegram_parser = TelegramParser

        self.telegram_parser = telegram_parser(telegram_specification)
        self.telegram_buffer = TelegramBuffer()

    def read(self):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's

        :rtype: generator
        """
        with serial.Serial(**self.serial_settings) as serial_handle:
            while True:
                data = serial_handle.readline()
                self.telegram_buffer.append(data.decode('ascii'))

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)


class AsyncSerialReader(SerialReader):
    """Serial reader using asyncio pyserial."""

    PORT_KEY = 'url'

    @asyncio.coroutine
    def read(self, queue):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's.

        Instead of being a generator, values are pushed to provided queue for
        asynchronous processing.

        :rtype: None
        """
        # create Serial StreamReader
        conn = serial_asyncio.open_serial_connection(**self.serial_settings)
        reader, _ = yield from conn

        while True:
            # Read line if available or give control back to loop until new
            # data has arrived.
            data = yield from reader.readline()
            self.telegram_buffer.append(data.decode('ascii'))

            for telegram in self.telegram_buffer.get_all():
                try:
                    # Push new parsed telegram onto queue.
                    queue.put_nowait(
                        self.telegram_parser.parse(telegram)
                    )
                except ParseError as e:
                    logger.warning('Failed to parse telegram: %s', e)
