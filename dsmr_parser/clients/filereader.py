import logging
import fileinput
import tailer

from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.parsers import TelegramParser

logger = logging.getLogger(__name__)


class FileReader(object):
    """
     Filereader to read and parse raw telegram strings from a file and instantiate Telegram objects
     for each read telegram.
     Usage:
        from dsmr_parser import telegram_specifications
        from dsmr_parser.clients.filereader import FileReader

        if __name__== "__main__":

            infile = '/data/smartmeter/readings.txt'

            file_reader = FileReader(
                file = infile,
                telegram_specification = telegram_specifications.V4
                )

            for telegram in file_reader.read_as_object():
                print(telegram)

     The file can be created like:
        from dsmr_parser import telegram_specifications
        from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5

        if __name__== "__main__":

            outfile = '/data/smartmeter/readings.txt'

            serial_reader = SerialReader(
                device='/dev/ttyUSB0',
                serial_settings=SERIAL_SETTINGS_V5,
                telegram_specification=telegram_specifications.V4
            )

            for telegram in serial_reader.read_as_object():
                f=open(outfile,"ab+")
                f.write(telegram._telegram_data.encode())
                f.close()
     """

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
        with open(self._file, "rb") as file_handle:
            while True:
                data = file_handle.readline()

                if not data:
                    break

                self.telegram_buffer.append(data.decode())

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)


class FileInputReader(object):
    """
     Filereader to read and parse raw telegram strings from stdin or files specified at the commandline
     and instantiate Telegram objects for each read telegram.
     Usage python script "syphon_smartmeter_readings_stdin.py":
        from dsmr_parser import telegram_specifications
        from dsmr_parser.clients.filereader import FileInputReader

        if __name__== "__main__":

            fileinput_reader = FileReader(
                file = infile,
                telegram_specification = telegram_specifications.V4
                )

            for telegram in fileinput_reader.read_as_object():
                print(telegram)

    Command line:
        tail -f /data/smartmeter/readings.txt | python3 syphon_smartmeter_readings_stdin.py

     """

    def __init__(self, telegram_specification):
        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_buffer = TelegramBuffer()
        self.telegram_specification = telegram_specification

    def read_as_object(self):
        """
        Read complete DSMR telegram's from stdin of filearguments specified on teh command line
        and return a Telegram object.
        :rtype: generator
        """
        with fileinput.input(mode='rb') as file_handle:
            while True:
                data = file_handle.readline()
                str = data.decode()
                self.telegram_buffer.append(str)

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)


class FileTailReader(object):
    """
      Filereader to read and parse raw telegram strings from the tail of a
      given file and instantiate Telegram objects for each read telegram.
      Usage python script "syphon_smartmeter_readings_stdin.py":
        from dsmr_parser import telegram_specifications
        from dsmr_parser.clients.filereader import FileTailReader

        if __name__== "__main__":

            infile = '/data/smartmeter/readings.txt'

            filetail_reader = FileTailReader(
                file = infile,
                telegram_specification = telegram_specifications.V5
                )

            for telegram in filetail_reader.read_as_object():
                print(telegram)
      """

    def __init__(self, file, telegram_specification):
        self._file = file
        self.telegram_parser = TelegramParser(telegram_specification)
        self.telegram_buffer = TelegramBuffer()
        self.telegram_specification = telegram_specification

    def read_as_object(self):
        """
        Read complete DSMR telegram's from a files tail and return a Telegram object.
        :rtype: generator
        """
        with open(self._file, "rb") as file_handle:
            for data in tailer.follow(file_handle):
                str = data.decode()
                self.telegram_buffer.append(str)

                for telegram in self.telegram_buffer.get_all():
                    try:
                        yield self.telegram_parser.parse(telegram)
                    except InvalidChecksumError as e:
                        logger.warning(str(e))
                    except ParseError as e:
                        logger.error('Failed to parse telegram: %s', e)
