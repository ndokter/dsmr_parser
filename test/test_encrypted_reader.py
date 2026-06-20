"""End-to-end tests: encrypted binary frames flowing through the readers.

These exercise the binary framing added on top of the general-global-cipher
decryption, i.e. that a raw 0xDB DLMS frame arriving on the transport is
assembled, decrypted and parsed (the path Home Assistant relies on via
``create_dsmr_reader`` / ``DSMRProtocol``).
"""
from decimal import Decimal
import unittest

from dsmr_parser import telegram_specifications
from dsmr_parser.clients.protocol import DSMRProtocol
from dsmr_parser.clients.serial_ import SerialReader
from dsmr_parser.clients.socket_ import SocketReader
from dsmr_parser.clients.telegram_buffer import EncryptedTelegramBuffer, TelegramBuffer
from dsmr_parser.exceptions import DecryptionError, ParseError
from dsmr_parser.parsers import TelegramParser
from test.encryption_helpers import build_general_global_cipher_frame
from test.example_telegrams import TELEGRAM_SAGEMCOM_T210_D_R

ENCRYPTION_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
AUTHENTICATION_KEY = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"


def _frame():
    return build_general_global_cipher_frame(
        TELEGRAM_SAGEMCOM_T210_D_R, ENCRYPTION_KEY, AUTHENTICATION_KEY
    )


class _FakeTransport:
    """Minimal asyncio transport stand-in that records close()."""

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


def _make_protocol(callback):
    return DSMRProtocol(
        None,
        TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R),
        telegram_callback=callback,
        encryption_key=ENCRYPTION_KEY,
        authentication_key=AUTHENTICATION_KEY,
    )


class DSMRProtocolEncryptedTest(unittest.TestCase):

    def test_selects_encrypted_buffer(self):
        protocol = _make_protocol(lambda telegram: None)
        self.assertIsInstance(protocol.telegram_buffer, EncryptedTelegramBuffer)

    def test_full_frame_decrypts_and_parses(self):
        telegrams = []
        protocol = _make_protocol(telegrams.append)

        protocol.data_received(_frame())

        self.assertEqual(len(telegrams), 1)
        self.assertEqual(
            telegrams[0].ELECTRICITY_IMPORTED_TOTAL.value, Decimal("6545766")
        )
        self.assertEqual(
            telegrams[0].CURRENT_ELECTRICITY_USAGE.value, Decimal("286")
        )

    def test_frame_chunked_across_data_received(self):
        telegrams = []
        protocol = _make_protocol(telegrams.append)
        frame = _frame()

        # Simulate the transport delivering the frame in several chunks.
        protocol.data_received(frame[:50])
        self.assertEqual(telegrams, [])
        protocol.data_received(frame[50:200])
        self.assertEqual(telegrams, [])
        protocol.data_received(frame[200:])

        self.assertEqual(len(telegrams), 1)
        self.assertEqual(
            telegrams[0].ELECTRICITY_IMPORTED_TOTAL.value, Decimal("6545766")
        )

    def test_wrong_key_tears_down_connection(self):
        # A wrong key is unrecoverable: the protocol must record the failure,
        # close the transport, and deliver no telegram (no spinning).
        telegrams = []
        protocol = DSMRProtocol(
            None,
            TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R),
            telegram_callback=telegrams.append,
            encryption_key="CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",  # wrong
            authentication_key=AUTHENTICATION_KEY,
        )
        transport = _FakeTransport()
        protocol.connection_made(transport)

        protocol.data_received(_frame())

        self.assertEqual(telegrams, [])
        self.assertIsInstance(protocol.decryption_error, DecryptionError)
        self.assertTrue(transport.closed)


class WrongKeyParseTest(unittest.TestCase):
    """A wrong key/corrupted frame must surface as a fatal DecryptionError."""

    def test_wrong_key_raises_decryption_error(self):
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)
        with self.assertRaises(DecryptionError):
            parser.parse(
                _frame().hex(),
                "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",  # wrong encryption key
                AUTHENTICATION_KEY,
            )

    def test_decryption_error_is_not_parse_error(self):
        # It must not be swallowed by generic `except ParseError` handlers.
        self.assertFalse(issubclass(DecryptionError, ParseError))


class ReaderBufferSelectionTest(unittest.TestCase):
    """Readers must pick the binary buffer for encrypted specs and frame correctly."""

    def test_serial_reader_uses_encrypted_buffer(self):
        reader = SerialReader(
            device="/dev/ttyUSB0",
            serial_settings={},
            telegram_specification=telegram_specifications.SAGEMCOM_T210_D_R,
            encryption_key=ENCRYPTION_KEY,
            authentication_key=AUTHENTICATION_KEY,
        )
        self.assertIsInstance(reader.telegram_buffer, EncryptedTelegramBuffer)
        telegrams = list(reader._buffer_incoming(_frame()))
        self.assertEqual(telegrams, [_frame().hex()])

    def test_serial_reader_plain_spec_uses_text_buffer(self):
        reader = SerialReader(
            device="/dev/ttyUSB0",
            serial_settings={},
            telegram_specification=telegram_specifications.V5,
        )
        self.assertIsInstance(reader.telegram_buffer, TelegramBuffer)

    def test_socket_reader_uses_encrypted_buffer(self):
        reader = SocketReader(
            host="localhost",
            port=2001,
            telegram_specification=telegram_specifications.SAGEMCOM_T210_D_R,
            encryption_key=ENCRYPTION_KEY,
            authentication_key=AUTHENTICATION_KEY,
        )
        self.assertIsInstance(reader.telegram_buffer, EncryptedTelegramBuffer)
        # Socket data is binary and must not be line-split for encrypted frames.
        telegrams = list(reader._buffer_incoming(_frame()))
        self.assertEqual(telegrams, [_frame().hex()])
