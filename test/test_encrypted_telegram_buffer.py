"""Tests for EncryptedTelegramBuffer (binary DLMS general-global-cipher framing)."""
import unittest

from dsmr_parser.clients.telegram_buffer import EncryptedTelegramBuffer
from test.encryption_helpers import build_general_global_cipher_frame
from test.example_telegrams import TELEGRAM_SAGEMCOM_T210_D_R

ENCRYPTION_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
AUTHENTICATION_KEY = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"


def _frame(invocation_counter=0x10000001):
    return build_general_global_cipher_frame(
        TELEGRAM_SAGEMCOM_T210_D_R,
        ENCRYPTION_KEY,
        AUTHENTICATION_KEY,
        invocation_counter=invocation_counter,
    )


class EncryptedTelegramBufferTest(unittest.TestCase):

    def test_single_complete_frame(self):
        frame = _frame()
        buffer = EncryptedTelegramBuffer()
        buffer.append(frame)

        telegrams = list(buffer.get_all())

        self.assertEqual(telegrams, [frame.hex()])

    def test_frame_split_across_appends(self):
        frame = _frame()
        buffer = EncryptedTelegramBuffer()

        # Feed the frame byte-by-byte; only the final byte completes it.
        for byte in frame[:-1]:
            buffer.append(bytes([byte]))
            self.assertEqual(list(buffer.get_all()), [])
        buffer.append(bytes([frame[-1]]))

        self.assertEqual(list(buffer.get_all()), [frame.hex()])

    def test_two_back_to_back_frames(self):
        frame1 = _frame(invocation_counter=0x10000001)
        frame2 = _frame(invocation_counter=0x10000002)
        buffer = EncryptedTelegramBuffer()
        buffer.append(frame1 + frame2)

        telegrams = list(buffer.get_all())

        self.assertEqual(telegrams, [frame1.hex(), frame2.hex()])

    def test_resync_on_leading_garbage(self):
        frame = _frame()
        buffer = EncryptedTelegramBuffer()
        # Random bytes before the real frame (none of which is 0xDB).
        buffer.append(b"\x00\x01\x02garbage" + frame)

        telegrams = list(buffer.get_all())

        self.assertEqual(telegrams, [frame.hex()])

    def test_incomplete_frame_yields_nothing(self):
        frame = _frame()
        buffer = EncryptedTelegramBuffer()
        buffer.append(frame[:20])  # header + a bit, but not the full payload

        self.assertEqual(list(buffer.get_all()), [])

    def test_partial_header_yields_nothing(self):
        buffer = EncryptedTelegramBuffer()
        buffer.append(b"\xdb\x08")  # only tag + system title length

        self.assertEqual(list(buffer.get_all()), [])
