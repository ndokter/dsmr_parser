import logging

import serialx

from dsmr_parser.clients.telegram_buffer import TelegramBuffer, EncryptedTelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.parsers import TelegramParser


logger = logging.getLogger(__name__)


class SerialReader(object):
    PORT_KEY = 'url'

    def __init__(self, device, serial_settings, telegram_specification,
                 encryption_key="", authentication_key=""):
        self.serial_settings = serial_settings
        self.serial_settings[self.PORT_KEY] = device

        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_specification = telegram_specification
        self._encryption_key = encryption_key
        self._authentication_key = authentication_key
        self._encrypted = bool(telegram_specification.get("general_global_cipher"))
        self.telegram_buffer = \
            EncryptedTelegramBuffer() if self._encrypted else TelegramBuffer()

    def _buffer_incoming(self, data):
        """
        Append raw transport bytes to the buffer and return the complete
        telegrams ready to be parsed. Encrypted telegrams are binary DLMS
        frames and must not be decoded; plain telegrams are ascii.
        :param bytes data:
        :rtype generator:
        """
        if self._encrypted:
            self.telegram_buffer.append(data)
        else:
            self.telegram_buffer.append(data.decode('ascii'))
        return self.telegram_buffer.get_all()

    def read(self):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's

        :rtype: generator
        """
        with serialx.serial_for_url(**self.serial_settings) as serial_handle:
            while True:
                data = serial_handle.read(max(1, min(1024, serial_handle.num_unread_bytes())))
                try:
                    telegrams = self._buffer_incoming(data)
                except Exception:
                    logger.warning('Failed to decode telegram data: %s', data)
                    continue

                for telegram in telegrams:
                    try:
                        yield self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    except InvalidChecksumError as e:
                        logger.info(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)

    def read_as_object(self):
        """
        Read complete DSMR telegram's from the serial interface and return a Telegram object.

        :rtype: generator
        """
        with serialx.serial_for_url(**self.serial_settings) as serial_handle:
            while True:
                data = serial_handle.readline()
                try:
                    telegrams = self._buffer_incoming(data)
                except Exception:
                    logger.warning('Failed to decode telegram data: %s', data)
                    continue

                for telegram in telegrams:
                    try:
                        yield self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)


class AsyncSerialReader(SerialReader):
    """Serial reader using asyncio serialx."""

    PORT_KEY = 'url'

    async def read(self, queue):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's.

        Instead of being a generator, values are pushed to provided queue for
        asynchronous processing.

        :rtype: None
        """
        # create Serial StreamReader
        conn = serialx.open_serial_connection(**self.serial_settings)
        reader, _ = await conn

        while True:
            # Read line if available or give control back to loop until new
            # data has arrived.
            data = await reader.readline()
            try:
                telegrams = self._buffer_incoming(data)
            except Exception:
                logger.warning('Failed to decode telegram data: %s', data)
                continue

            for telegram in telegrams:
                try:
                    # Push new parsed telegram onto queue.
                    queue.put_nowait(
                        self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    )
                except ParseError as e:
                    logger.warning('Failed to parse telegram: %s', e)

    async def read_as_object(self, queue):
        """
        Read complete DSMR telegram's from the serial interface
        and return a Telegram object.

        Instead of being a generator, Telegram objects are pushed
        to provided queue for asynchronous processing.

        :rtype: None
        """

        # create Serial StreamReader
        conn = serialx.open_serial_connection(**self.serial_settings)
        reader, _ = await conn

        while True:

            # Read line if available or give control back to loop until new
            # data has arrived.
            data = await reader.readline()
            try:
                telegrams = self._buffer_incoming(data)
            except Exception:
                logger.warning('Failed to decode telegram data: %s', data)
                continue

            for telegram in telegrams:
                try:
                    queue.put_nowait(
                        self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    )
                except InvalidChecksumError as e:
                    logger.warning(str(e))
                except ParseError as e:
                    logger.error('Failed to parse telegram: %s', e)
