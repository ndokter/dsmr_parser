from binascii import unhexlify
from copy import deepcopy

import unittest

from dlms_cosem.exceptions import DecryptionError
from dlms_cosem.protocol.xdlms import GeneralGlobalCipher
from dlms_cosem.security import SecurityControlField, encrypt

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import ParseError
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_SAGEMCOM_T210_D_R


class TelegramParserEncryptedTest(unittest.TestCase):
    """ Test parsing of a DSML encypted DSMR v5.x telegram. """
    DUMMY_ENCRYPTION_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    DUMMY_AUTHENTICATION_KEY = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"

    def __generate_encrypted(self, security_suite=0, authenticated=True, encrypted=True):
        security_control = SecurityControlField(
            security_suite=security_suite, authenticated=authenticated, encrypted=encrypted
        )
        encryption_key = unhexlify(self.DUMMY_ENCRYPTION_KEY)
        authentication_key = unhexlify(self.DUMMY_AUTHENTICATION_KEY)
        system_title = "SYSTEMID".encode("ascii")
        invocation_counter = int.from_bytes(bytes.fromhex("10000001"), "big")
        plain_data = TELEGRAM_SAGEMCOM_T210_D_R.encode("ascii")

        encrypted = encrypt(
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
        full_frame.extend([0x82])  # Length of the following length bytes
        # https://github.com/pwitab/dlms-cosem/blob/739f81a58e5f07663a512d4a128851333a0ed5e6/dlms_cosem/a_xdr.py#L33

        security_control = security_control.to_bytes()
        invocation_counter = invocation_counter.to_bytes(4, "big", signed=False)
        full_frame.extend((len(encrypted)
                           + len(invocation_counter)
                           + len(security_control)).to_bytes(2, "big", signed=False))
        full_frame.extend(security_control)
        full_frame.extend(invocation_counter)
        full_frame.extend(encrypted)

        return full_frame

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)
        result = parser.parse(self.__generate_encrypted().hex(),
                              self.DUMMY_ENCRYPTION_KEY,
                              self.DUMMY_AUTHENTICATION_KEY)
        self.assertEqual(len(result), 18)

    def test_damaged_frame(self):
        # If the frame is damaged decrypting fails (crc is technically not needed)
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)

        generated = self.__generate_encrypted()
        generated[150] = 0x00
        generated = generated.hex()

        with self.assertRaises(DecryptionError):
            parser.parse(generated, self.DUMMY_ENCRYPTION_KEY, self.DUMMY_AUTHENTICATION_KEY)

    def test_plain(self):
        # If a plain request is parsed with "general_global_cipher": True it fails
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)

        with self.assertRaises(Exception):
            parser.parse(TELEGRAM_SAGEMCOM_T210_D_R, self.DUMMY_ENCRYPTION_KEY, self.DUMMY_AUTHENTICATION_KEY)

    def test_general_global_cipher_not_specified(self):
        # If a GGC frame is detected but general_global_cipher is not set it fails
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)
        parser = deepcopy(parser)  # We do not want to change the module value
        parser.telegram_specification['general_global_cipher'] = False

        with self.assertRaises(ParseError):
            parser.parse(self.__generate_encrypted().hex(), self.DUMMY_ENCRYPTION_KEY, self.DUMMY_AUTHENTICATION_KEY)

    def test_only_encrypted(self):
        # Not implemented by dlms_cosem
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)

        only_auth = self.__generate_encrypted(0, authenticated=False, encrypted=True).hex()

        with self.assertRaises(ValueError):
            parser.parse(only_auth, self.DUMMY_ENCRYPTION_KEY)

    def test_only_auth(self):
        # Not implemented by dlms_cosem
        parser = TelegramParser(telegram_specifications.SAGEMCOM_T210_D_R)

        only_auth = self.__generate_encrypted(0, authenticated=True, encrypted=False).hex()

        with self.assertRaises(ValueError):
            parser.parse(only_auth, authentication_key=self.DUMMY_AUTHENTICATION_KEY)
