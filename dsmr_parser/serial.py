import asyncio
import logging
import serial
import serial_asyncio

from dsmr_parser.exceptions import ParseError
from dsmr_parser.parsers import TelegramParser, TelegramParserV2_2, \
    TelegramParserV4

logger = logging.getLogger(__name__)


SERIAL_SETTINGS_V2_2 = {
    'baudrate': 9600,
    'bytesize': serial.SEVENBITS,
    'parity': serial.PARITY_EVEN,
    'stopbits': serial.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}

SERIAL_SETTINGS_V4 = {
    'baudrate': 115200,
    'bytesize': serial.SEVENBITS,
    'parity': serial.PARITY_EVEN,
    'stopbits': serial.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}


def is_start_of_telegram(line):
    """
    :type line: line
    """
    return line.startswith('/')


def is_end_of_telegram(line):
    """
    :type line: line
    """
    return line.startswith('!')


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

    def read(self):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's

        :rtype dict
        """
        with serial.Serial(**self.serial_settings) as serial_handle:
            telegram = []

            while True:
                line = serial_handle.readline()
                line = line.decode('ascii')  # TODO move this to the parser?

                # Telegrams need to be complete because the values belong to a
                # particular reading and can also be related to eachother.
                if not telegram and not is_start_of_telegram(line):
                    continue

                telegram.append(line)

                if is_end_of_telegram(line):

                    try:
                        yield self.telegram_parser.parse(telegram)
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)

                    telegram = []


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

        :rtype Generator/Async
        """
        # create Serial StreamReader
        conn = serial_asyncio.open_serial_connection(**self.serial_settings)
        reader, _ = yield from conn

        telegram = []

        while True:
            # read line if available or give control back to loop until
            # new data has arrived
            line = yield from reader.readline()
            line = line.decode('ascii')

            # Telegrams need to be complete because the values belong to a
            # particular reading and can also be related to eachother.
            if not telegram and not is_start_of_telegram(line):
                continue

            telegram.append(line)

            if is_end_of_telegram(line):
                try:
                    parsed_telegram = self.telegram_parser.parse(telegram)
                    # push new parsed telegram onto queue
                    queue.put_nowait(parsed_telegram)
                except ParseError as e:
                    logger.warning('Failed to parse telegram: %s', e)

                telegram = []
