import logging
import socket

from dsmr_parser.clients.telegram_buffer import TelegramBuffer, EncryptedTelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.parsers import TelegramParser


logger = logging.getLogger(__name__)


class SocketReader(object):

    BUFFER_SIZE = 256

    def __init__(self, host, port, telegram_specification,
                 encryption_key="", authentication_key=""):
        self.host = host
        self.port = port

        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_specification = telegram_specification
        self._encryption_key = encryption_key
        self._authentication_key = authentication_key
        self._encrypted = bool(telegram_specification.get("general_global_cipher"))
        self.telegram_buffer = \
            EncryptedTelegramBuffer() if self._encrypted else TelegramBuffer()

    def _buffer_incoming(self, data):
        """
        Append raw bytes received from the socket to the buffer and return the
        complete telegrams ready to be parsed. Encrypted telegrams are binary
        DLMS frames and are buffered as raw bytes; plain telegrams are split
        into ascii lines (tolerating garbage as before).
        :param bytes data:
        :rtype generator:
        """
        if self._encrypted:
            self.telegram_buffer.append(data)
        else:
            for line in data.splitlines(keepends=True):
                try:
                    self.telegram_buffer.append(line.decode('ascii'))
                except UnicodeDecodeError:
                    # Some garbage came through the channel
                    # E.g.: Happens at EON_HUNGARY, but only once at the start.
                    logger.error('Failed to parse telegram due to unicode decode error')
        return self.telegram_buffer.get_all()

    def read(self):
        """
        Read complete DSMR telegram's from remote interface and parse it
        into CosemObject's and MbusObject's

        :rtype: generator
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_handle:
            socket_handle.settimeout(60)
            socket_handle.connect((self.host, self.port))

            while True:
                try:
                    data = socket_handle.recv(self.BUFFER_SIZE)
                except socket.timeout:
                    logger.error("Socket timeout occurred, exiting")
                    break

                for telegram in self._buffer_incoming(data):
                    try:
                        yield self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    except InvalidChecksumError as e:
                        logger.info(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)

    def read_as_object(self):
        """
        Read complete DSMR telegram's from remote and return a Telegram object.

        :rtype: generator
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_handle:

            socket_handle.connect((self.host, self.port))

            while True:
                data = socket_handle.recv(self.BUFFER_SIZE)

                for telegram in self._buffer_incoming(data):
                    try:
                        yield self.telegram_parser.parse(
                            telegram, self._encryption_key, self._authentication_key)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)
