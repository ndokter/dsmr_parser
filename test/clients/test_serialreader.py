import unittest
import tempfile
from unittest import mock

from dsmr_parser import telegram_specifications
from dsmr_parser.clients.filereader import FileReader
from dsmr_parser.clients.serial_ import SerialReader
from dsmr_parser.clients.settings import SERIAL_SETTINGS_V5

from test.example_telegrams import TELEGRAM_V5


class SerialReaderTest(unittest.TestCase):

    @mock.patch('dsmr_parser.clients.serial_.serial.Serial')
    def test_read_as_object(self, mock_serial):
        serial_handle_mock = mock_serial.return_value
        # mock_serial.return_value.in_waiting = 1024
        mock_serial.return_value.read.return_value = [b'Telegram data...', b'']  # Return data, then empty bytes


        serial_reader = SerialReader(
            device='/dev/ttyUSB0',
            serial_settings=SERIAL_SETTINGS_V5,
            telegram_specification=telegram_specifications.V5
        )
        
        for telegram in serial_reader.read():
            print(telegram)  # see 'Telegram object' docs below