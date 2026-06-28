"""Tests for the authentication_key=None opt-in (decrypt without verification).

When ``authentication_key=None`` is passed, the parser decrypts a
general-global-cipher telegram using only the encryption key and does not
verify the GCM authentication tag (integrity comes from the telegram CRC).
This is needed for meters whose authentication key is unknown or differs from
the spec's (e.g. the Luxembourg Smarty), and matches what ESPHome does.
"""
from binascii import unhexlify
from decimal import Decimal

import unittest

from dlms_cosem.protocol.xdlms import GeneralGlobalCipher
from dlms_cosem.security import SecurityControlField, encrypt

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import DecryptionError
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_LUXEMBOURG_SMARTY

ENCRYPTION_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
# An authentication key the caller does NOT know -- as on a real meter whose
# auth key is not the fixed one in the spec.
METER_AUTHENTICATION_KEY = "0102030405060708090A0B0C0D0E0F10"


def _build_frame(encryption_key, authentication_key):
    security_control = SecurityControlField(
        security_suite=0, authenticated=True, encrypted=True
    )
    system_title = b"SYSTEMID"
    invocation_counter = int.from_bytes(bytes.fromhex("10000001"), "big")
    encrypted_data = encrypt(
        security_control=security_control,
        key=unhexlify(encryption_key),
        auth_key=unhexlify(authentication_key),
        system_title=system_title,
        invocation_counter=invocation_counter,
        plain_text=TELEGRAM_LUXEMBOURG_SMARTY.encode("ascii"),
    )
    frame = bytearray(GeneralGlobalCipher.TAG.to_bytes(1, "big"))
    frame.extend(len(system_title).to_bytes(1, "big"))
    frame.extend(system_title)
    frame.append(0x82)
    sc = security_control.to_bytes()
    ic = invocation_counter.to_bytes(4, "big")
    frame.extend((len(sc) + len(ic) + len(encrypted_data)).to_bytes(2, "big"))
    frame.extend(sc)
    frame.extend(ic)
    frame.extend(encrypted_data)
    return frame.hex()


class DecryptWithoutVerificationTest(unittest.TestCase):

    def test_decrypts_regardless_of_authentication_key(self):
        # Encrypted with an authentication key the caller does not have.
        frame = _build_frame(ENCRYPTION_KEY, METER_AUTHENTICATION_KEY)
        parser = TelegramParser(telegram_specifications.MSN)

        result = parser.parse(frame, ENCRYPTION_KEY, authentication_key=None)

        self.assertEqual(
            result[obis.ELECTRICITY_IMPORTED_TOTAL].value, Decimal("273.764")
        )

    def test_wrong_encryption_key_is_rejected(self):
        frame = _build_frame(ENCRYPTION_KEY, METER_AUTHENTICATION_KEY)
        parser = TelegramParser(telegram_specifications.MSN)

        with self.assertRaises(DecryptionError):
            parser.parse(frame, "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", authentication_key=None)

    def test_authenticated_default_still_verifies(self):
        # With a string authentication key the GCM tag is still verified: a
        # wrong key must fail (the default behaviour is unchanged).
        frame = _build_frame(ENCRYPTION_KEY, METER_AUTHENTICATION_KEY)
        parser = TelegramParser(telegram_specifications.MSN)

        with self.assertRaises(DecryptionError):
            parser.parse(frame, ENCRYPTION_KEY, "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")


if __name__ == "__main__":
    unittest.main()
