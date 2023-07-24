import logging
import socket

from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.parsers import TelegramParser


logger = logging.getLogger(__name__)


class SocketReader(object):

    BUFFER_SIZE = 256

    def __init__(self, host, port, telegram_specification):
        self.host = host
        self.port = port

        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_buffer = TelegramBuffer()
        self.telegram_specification = telegram_specification

    def read(self):
        """
        Read complete DSMR telegram's from remote interface and parse it
        into CosemObject's and MbusObject's

        :rtype: generator
        """
        buffer = b""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_handle:

            socket_handle.connect((self.host, self.port))

            while True:
                buffer += socket_handle.recv(self.BUFFER_SIZE)

                lines = buffer.splitlines(keepends=True)

                if len(lines) == 0:
                    continue

                for data in lines:
                    try:
                        self.telegram_buffer.append(data.decode('ascii'))
                    except UnicodeDecodeError:
                        # Some garbage came through the channel
                        # E.g.: Happens at EON_HUNGARY, but only once at the start of the socket.
                        logger.error('Failed to parse telegram due to unicode decode error')

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)

                buffer = b""

    def read_as_object(self):
        """
        Read complete DSMR telegram's from remote and return a Telegram object.

        :rtype: generator
        """
        buffer = b""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_handle:

            socket_handle.connect((self.host, self.port))

            while True:
                buffer += socket_handle.recv(self.BUFFER_SIZE)

                lines = buffer.splitlines(keepends=True)

                if len(lines) == 0:
                    continue

                for data in lines:
                    self.telegram_buffer.append(data.decode('ascii'))

                    for telegram in self.telegram_buffer.get_all():
                        try:
                            yield self.telegram_parser.parse(telegram)
                        except InvalidChecksumError as e:
                            logger.warning(str(e))
                        except ParseError as e:
                            logger.error('Failed to parse telegram: %s', e)

                buffer = b""
