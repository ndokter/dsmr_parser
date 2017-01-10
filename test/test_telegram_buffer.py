import unittest

from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from test.example_telegrams import TELEGRAM_V2_2, TELEGRAM_V4_2


class TelegramBufferTest(unittest.TestCase):

    def setUp(self):
        self.telegram_buffer = TelegramBuffer()

    def test_v22_telegram(self):
        self.telegram_buffer.append(TELEGRAM_V2_2)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V2_2)
        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_v42_telegram(self):
        self.telegram_buffer.append(TELEGRAM_V4_2)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_multiple_mixed_telegrams(self):
        self.telegram_buffer.append(
            ''.join((TELEGRAM_V2_2, TELEGRAM_V4_2, TELEGRAM_V2_2))
        )

        telegrams = list(self.telegram_buffer.get_all())

        self.assertListEqual(
            telegrams,
            [
                TELEGRAM_V2_2,
                TELEGRAM_V4_2,
                TELEGRAM_V2_2
            ]
        )

        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_v42_telegram_preceded_with_unclosed_telegram(self):
        # There are unclosed telegrams at the start of the buffer.
        incomplete_telegram = TELEGRAM_V4_2[:-1]

        self.telegram_buffer.append(incomplete_telegram + TELEGRAM_V4_2)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_v42_telegram_preceded_with_unopened_telegram(self):
        # There is unopened telegrams at the start of the buffer indicating that
        # the buffer was being filled while the telegram was outputted halfway.
        incomplete_telegram = TELEGRAM_V4_2[1:]

        self.telegram_buffer.append(incomplete_telegram + TELEGRAM_V4_2)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_v42_telegram_trailed_by_unclosed_telegram(self):
        incomplete_telegram = TELEGRAM_V4_2[:-1]

        self.telegram_buffer.append(TELEGRAM_V4_2 + incomplete_telegram)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, incomplete_telegram)

    def test_v42_telegram_trailed_by_unopened_telegram(self):
        incomplete_telegram = TELEGRAM_V4_2[1:]

        self.telegram_buffer.append(TELEGRAM_V4_2 + incomplete_telegram)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, incomplete_telegram)

    def test_v42_telegram_adding_line_by_line(self):
        for line in TELEGRAM_V4_2.splitlines(keepends=True):
            self.telegram_buffer.append(line)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, '')

    def test_v42_telegram_adding_char_by_char(self):
        for char in TELEGRAM_V4_2:
            self.telegram_buffer.append(char)

        telegram = next(self.telegram_buffer.get_all())

        self.assertEqual(telegram, TELEGRAM_V4_2)
        self.assertEqual(self.telegram_buffer._buffer, '')
