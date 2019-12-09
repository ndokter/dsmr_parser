import logging

from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.objects import Telegram
from dsmr_parser.parsers import TelegramParser

logger = logging.getLogger(__name__)

class FileReader(object):

    def __init__(self, file, telegram_specification):
        self._file = file
        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_buffer = TelegramBuffer()
        self.telegram_specification = telegram_specification

    def read_as_object(self):
        """
        Read complete DSMR telegram's from a file and return a Telegram object.
        :rtype: generator
        """
        with open(self._file,"rb") as file_handle:
            while True:
                data = file_handle.readline()
                str = data.decode()
                self.telegram_buffer.append(str)

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield Telegram(telegram, self.telegram_parser, self.telegram_specification)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)
