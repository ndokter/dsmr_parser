import asyncio
import logging
import re
import serial
import serial_asyncio

from .exceptions import ParseError
from .parsers import TelegramParser, TelegramParserV2_2, TelegramParserV4

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


class TelegramBuffer(object):
    """
    Used as a buffer for a stream of telegram data. Constructs full telegram
    strings from the buffered data and returns it.
    """

    def __init__(self):
        self._buffer = ''

    def get_all(self):
        """
        Remove complete telegrams from buffer and yield them.
        :rtype generator:
        """
        for telegram in self._find_telegrams():
            self._remove(telegram)
            yield telegram

    def append(self, data):
        """
        Add telegram data to buffer.
        :param str data: chars, lines or full telegram strings of telegram data
        """
        self._buffer += data

    def _remove(self, telegram):
        """
        Remove telegram from buffer and incomplete data preceding it. This
        is easier than validating the data before adding it to the buffer.
        :param str telegram:
        :return:
        """
        # Remove data leading up to the telegram and the telegram itself.
        index = self._buffer.index(telegram) + len(telegram)

        self._buffer = self._buffer[index:]

    def _find_telegrams(self):
        """
        Find complete telegrams in buffer from  start ('/') till ending
        checksum ('!AB12\r\n').
        :rtype: list
        """
        # - Match all characters after start of telegram except for the start
        # itself again '^\/]+', which eliminates incomplete preceding telegrams.
        # - Do non greedy match using '?' so start is matched up to the first
        # checksum that's found.
        # - The checksum is optional '{0,4}' because not all telegram versions
        # support it.
        return re.findall(
            r'\/[^\/]+?\![A-F0-9]{0,4}\r\n',
            self._buffer,
            re.DOTALL
        )
