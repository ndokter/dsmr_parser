import unittest
import tempfile

from dsmr_parser.clients.filereader import FileReader
from dsmr_parser.telegram_specifications import V5
from test.example_telegrams import TELEGRAM_V5


class FileReaderTest(unittest.TestCase):
    def test_read_as_object(self):
        with tempfile.NamedTemporaryFile() as file:
            with open(file.name, "w") as f:
                f.write(TELEGRAM_V5)

            telegrams = []
            reader = FileReader(file=file.name, telegram_specification=V5)
            # Call
            for telegram in reader.read_as_object():
                telegrams.append(telegram)

            self.assertEqual(len(telegrams), 1)
