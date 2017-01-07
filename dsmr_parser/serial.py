import asyncio
import logging
import re
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
    :param bytes line: series of bytes representing a line.
        Example: b'/KFM5KAIFA-METER\r\n'
    """
    return line.startswith('/')


def is_end_of_telegram(line):
    """
    :param bytes line: series of bytes representing a line.
        Example: b'!7B05\r\n'
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

        :rtype: generator
        """
        with serial.Serial(**self.serial_settings) as serial_handle:
            telegram = ''

            while True:
                line = serial_handle.readline()
                line.decode('ascii')

                # Build up buffer from the start of the telegram.
                if not telegram and not is_start_of_telegram(line):
                    continue

                telegram += line

                if is_end_of_telegram(line):
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)

                    telegram = ''


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

        telegram = ''

        while True:
            # Read line if available or give control back to loop until new
            # data has arrived.
            line = yield from reader.readline()
            line = line.decode('ascii')

            # Build up buffer from the start of the telegram.
            if not telegram and not is_start_of_telegram(line):
                continue

            telegram += line

            if is_end_of_telegram(line):
                try:
                    # Push new parsed telegram onto queue.
                    queue.put_nowait(
                        self.telegram_parser.parse(telegram)
                    )
                except ParseError as e:
                    logger.warning('Failed to parse telegram: %s', e)

                telegram = ''


class TelegramBuffer(object):

    def __init__(self, callback):
        self._callback = callback
        self._buffer = ''

    def append(self, data):
        """
        Add telegram data to buffer. The callback is called with a full telegram
        when data is complete.
        :param str data: chars or lines of telegram data
        :return:
        """
        self._buffer += data

        for telegram in self.find_telegrams(self._buffer):
            self._callback(telegram)
            self._remove(telegram)

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

    @staticmethod
    def find_telegrams(buffer):
        """
        Find complete telegrams from buffer from  start ('/') till ending
        checksum ('!AB12\r\n').
        :rtype: list
        """
        # - Match all characters after start of telegram except for the start
        # itself again '^\/]+', which eliminates incomplete preceding telegrams.
        # - Do non greedy match using '?' so start is matched up to the first
        # checksum that's found.
        # - The checksum is optional '{0,4}' because not all telegram versions
        # support it.
        return re.findall(r'\/[^\/]+?\![A-F0-9]{0,4}\r\n', buffer, re.DOTALL)
