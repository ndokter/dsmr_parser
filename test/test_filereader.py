import io
import unittest
import tempfile
from unittest.mock import patch

from dsmr_parser.clients.filereader import FileReader, FileInputReader, FileTailReader
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


class FileInputReaderTest(unittest.TestCase):
    def test_bad_checksum_is_logged_and_next_telegram_is_parsed(self):
        # Alter a protected voltage without updating the original checksum.
        corrupt = TELEGRAM_V5.replace('0230.0*V', '0231.0*V', 1)
        self.assertNotEqual(corrupt, TELEGRAM_V5)
        with tempfile.NamedTemporaryFile() as file:
            file.write((corrupt + TELEGRAM_V5).encode())
            file.flush()
            with patch('sys.argv', ['reader', file.name]):
                telegrams = FileInputReader(V5).read_as_object()
                try:
                    with self.assertLogs('dsmr_parser.clients.filereader', level='WARNING') as logs:
                        telegram = next(telegrams)
                    self.assertIn('CRC checksum', logs.output[0])
                    self.assertEqual(telegram.P1_MESSAGE_HEADER.value, '50')
                finally:
                    telegrams.close()

    def test_valid_stdin_telegram_is_unchanged(self):
        with patch('sys.argv', ['reader', '-']):
            with patch('sys.stdin', io.TextIOWrapper(io.BytesIO(TELEGRAM_V5.encode()))):
                telegrams = FileInputReader(V5).read_as_object()
                try:
                    self.assertEqual(next(telegrams).P1_MESSAGE_HEADER.value, '50')
                finally:
                    telegrams.close()


class FileTailReaderTest(unittest.TestCase):
    def test_bad_checksum_is_logged_and_next_telegram_is_parsed(self):
        corrupt = TELEGRAM_V5.replace('0230.0*V', '0231.0*V', 1)
        with tempfile.NamedTemporaryFile() as file:
            file.write((corrupt + TELEGRAM_V5).encode())
            file.flush()
            # Use the real file contents without tailer's indefinite wait at EOF.
            with patch('dsmr_parser.clients.filereader.tailer.follow', side_effect=iter):
                with self.assertLogs('dsmr_parser.clients.filereader', level='WARNING') as logs:
                    telegrams = list(FileTailReader(file.name, V5).read_as_object())
            self.assertIn('CRC checksum', logs.output[0])
            self.assertEqual(len(telegrams), 1)
            self.assertEqual(telegrams[0].P1_MESSAGE_HEADER.value, '50')
