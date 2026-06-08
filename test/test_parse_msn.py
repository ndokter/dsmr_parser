"""Tests for the MSN (Luxembourg Smarty encrypted) telegram specification.

Per the official Luxmetering E-Meter P1 Specification v1.1.3 (section 3.2.5),
the authentication key is fixed and identical for all Smarty meters:
    AAD = 0x30 || 00112233445566778899AABBCCDDEEFF
This key is hardcoded in the MSN telegram specification, so callers only need
to supply the per-meter encryption key obtained from their DSO.
"""
from binascii import unhexlify
from copy import deepcopy
from decimal import Decimal

import unittest

from dlms_cosem.protocol.xdlms import GeneralGlobalCipher
from dlms_cosem.security import SecurityControlField, encrypt

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import ParseError, DecryptionError
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_LUXEMBOURG_SMARTY

# Fixed authentication key for all Luxmetering Smarty meters (public, per spec 3.2.5)
LUXMETERING_AUTHENTICATION_KEY = "00112233445566778899AABBCCDDEEFF"


class TelegramParserMSNTest(unittest.TestCase):
    """Test parsing of MSN (Luxembourg Smarty encrypted) telegrams."""

    DUMMY_ENCRYPTION_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    def __generate_encrypted(self, security_suite=0, authenticated=True, encrypted=True):
        """Encrypt the example telegram using dummy enc key + fixed Luxmetering auth key."""
        security_control = SecurityControlField(
            security_suite=security_suite, authenticated=authenticated, encrypted=encrypted
        )
        encryption_key = unhexlify(self.DUMMY_ENCRYPTION_KEY)
        authentication_key = unhexlify(LUXMETERING_AUTHENTICATION_KEY)
        system_title = "SYSTEMID".encode("ascii")
        invocation_counter = int.from_bytes(bytes.fromhex("10000001"), "big")
        plain_data = TELEGRAM_LUXEMBOURG_SMARTY.encode("ascii")

        encrypted_data = encrypt(
            security_control=security_control,
            key=encryption_key,
            auth_key=authentication_key,
            system_title=system_title,
            invocation_counter=invocation_counter,
            plain_text=plain_data,
        )

        full_frame = bytearray(GeneralGlobalCipher.TAG.to_bytes(1, "big", signed=False))
        full_frame.extend(len(system_title).to_bytes(1, "big", signed=False))
        full_frame.extend(system_title)
        full_frame.extend([0x82])
        security_control_bytes = security_control.to_bytes()
        invocation_counter_bytes = invocation_counter.to_bytes(4, "big", signed=False)
        full_frame.extend((len(encrypted_data)
                           + len(invocation_counter_bytes)
                           + len(security_control_bytes)).to_bytes(2, "big", signed=False))
        full_frame.extend(security_control_bytes)
        full_frame.extend(invocation_counter_bytes)
        full_frame.extend(encrypted_data)

        return full_frame

    def test_msn_spec_has_general_global_cipher(self):
        """MSN spec must have general_global_cipher set to True."""
        self.assertTrue(telegram_specifications.MSN.get('general_global_cipher'))

    def test_msn_spec_has_embedded_authentication_key(self):
        """MSN spec must embed the fixed Luxmetering authentication key."""
        self.assertEqual(
            telegram_specifications.MSN.get('authentication_key'),
            LUXMETERING_AUTHENTICATION_KEY
        )

    def test_msn_spec_contains_luxembourg_smarty_objects(self):
        """MSN spec must contain all objects from LUXEMBOURG_SMARTY."""
        smarty_refs = {o['obis_reference'] for o in telegram_specifications.LUXEMBOURG_SMARTY['objects']}
        msn_refs = {o['obis_reference'] for o in telegram_specifications.MSN['objects']}
        self.assertTrue(smarty_refs.issubset(msn_refs))

    def test_parse_encrypted_with_encryption_key_only(self):
        """Encrypted MSN telegram should parse with only the per-meter encryption key.

        The authentication key is fixed per spec and embedded in the MSN spec —
        callers do not need to supply it.
        """
        parser = TelegramParser(telegram_specifications.MSN)
        result = parser.parse(
            self.__generate_encrypted().hex(),
            encryption_key=self.DUMMY_ENCRYPTION_KEY,
        )
        self.assertGreater(len(result), 0)

    def test_parse_values(self):
        """Parsed MSN telegram should contain expected OBIS values from the example telegram."""
        parser = TelegramParser(telegram_specifications.MSN)
        result = parser.parse(
            self.__generate_encrypted().hex(),
            encryption_key=self.DUMMY_ENCRYPTION_KEY,
        )
        # Total imported energy (P+)
        self.assertEqual(result[obis.ELECTRICITY_IMPORTED_TOTAL].value, Decimal('273.764'))
        # Total exported energy (P-)
        self.assertEqual(result[obis.ELECTRICITY_EXPORTED_TOTAL].value, Decimal('112743.030'))
        # Reactive imported total (Q+)
        self.assertEqual(result[obis.ELECTRICITY_REACTIVE_IMPORTED_TOTAL].value, Decimal('462.590'))
        # Instantaneous apparent power S+
        self.assertEqual(result[obis.MSN_INSTANTANEOUS_APPARENT_POWER_NEGATIVE].value, Decimal('0.913'))
        # Gas meter reading (optional — only present if an MBus slave is installed)
        self.assertEqual(result[obis.MBUS_METER_READING].value, Decimal('14239.771'))

    def test_parse_without_gas_meter(self):
        """MSN telegram without MBus slave (no gas meter) should parse successfully.

        The gas meter is an optional MBus slave device — not every Smarty
        installation has one connected.  The parser must still return a valid
        result; MBUS_METER_READING simply won't be present.
        """
        # Strip all MBus-related lines from the example telegram and recompute CRC
        mbus_prefixes = ('0-1:24.1.0', '0-1:96.1.0', '0-1:24.2.1', '0-1:24.4.0')
        lines = TELEGRAM_LUXEMBOURG_SMARTY.splitlines(keepends=True)
        body_lines = [
            line for line in lines
            if not any(line.startswith(p) for p in mbus_prefixes)
            and not line.startswith('!')
        ]
        body = ''.join(body_lines)
        # Recompute CRC over the body up to and including '!'
        crc = TelegramParser.crc16(body + '!')
        telegram_no_gas = body + '!{:04X}\r\n'.format(crc)

        security_control = SecurityControlField(security_suite=0, authenticated=True, encrypted=True)
        encryption_key = unhexlify(self.DUMMY_ENCRYPTION_KEY)
        authentication_key = unhexlify(LUXMETERING_AUTHENTICATION_KEY)
        system_title = "SYSTEMID".encode("ascii")
        invocation_counter = int.from_bytes(bytes.fromhex("10000001"), "big")

        encrypted_data = encrypt(
            security_control=security_control,
            key=encryption_key,
            auth_key=authentication_key,
            system_title=system_title,
            invocation_counter=invocation_counter,
            plain_text=telegram_no_gas.encode("ascii"),
        )
        full_frame = bytearray(GeneralGlobalCipher.TAG.to_bytes(1, "big", signed=False))
        full_frame.extend(len(system_title).to_bytes(1, "big", signed=False))
        full_frame.extend(system_title)
        full_frame.extend([0x82])
        sc_bytes = security_control.to_bytes()
        ic_bytes = invocation_counter.to_bytes(4, "big", signed=False)
        full_frame.extend((len(encrypted_data) + len(ic_bytes) + len(sc_bytes)).to_bytes(2, "big", signed=False))
        full_frame.extend(sc_bytes)
        full_frame.extend(ic_bytes)
        full_frame.extend(encrypted_data)

        parser = TelegramParser(telegram_specifications.MSN)
        result = parser.parse(full_frame.hex(), encryption_key=self.DUMMY_ENCRYPTION_KEY)

        self.assertGreater(len(result), 0)
        self.assertNotIn(obis.MBUS_METER_READING, result)
        # Core electricity values are still present
        self.assertEqual(result[obis.ELECTRICITY_IMPORTED_TOTAL].value, Decimal('273.764'))

    def test_damaged_frame(self):
        """Damaged encrypted frame should raise DecryptionError."""
        parser = TelegramParser(telegram_specifications.MSN)
        generated = self.__generate_encrypted()
        generated[150] = 0x00
        with self.assertRaises(DecryptionError):
            parser.parse(generated.hex(), self.DUMMY_ENCRYPTION_KEY)

    def test_plain_frame_fails(self):
        """Passing a plain (unencrypted) telegram to MSN parser should fail."""
        parser = TelegramParser(telegram_specifications.MSN)
        with self.assertRaises(Exception):
            parser.parse(TELEGRAM_LUXEMBOURG_SMARTY, self.DUMMY_ENCRYPTION_KEY)

    def test_general_global_cipher_false_fails(self):
        """GGC frame with general_global_cipher=False should raise ParseError."""
        parser = TelegramParser(telegram_specifications.MSN)
        parser = deepcopy(parser)
        parser.telegram_specification['general_global_cipher'] = False
        with self.assertRaises(ParseError):
            parser.parse(self.__generate_encrypted().hex(), self.DUMMY_ENCRYPTION_KEY)
