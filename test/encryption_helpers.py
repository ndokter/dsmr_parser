"""Test helpers for building encrypted (DLMS general-global-cipher) frames.

These mirror the on-the-wire framing of encrypted DSMR telegrams as emitted by
e.g. Luxembourg Smarty and Austrian Sagemcom meters, so tests can feed
realistic binary frames through the readers/buffers.
"""
from binascii import unhexlify

from dlms_cosem.protocol.xdlms import GeneralGlobalCipher
from dlms_cosem.security import SecurityControlField, encrypt


def build_general_global_cipher_frame(
    plain_text,
    encryption_key,
    authentication_key,
    system_title=b"SYSTEMID",
    invocation_counter=0x10000001,
    security_suite=0,
    authenticated=True,
    encrypted=True,
):
    """Encrypt ``plain_text`` and wrap it in a general-global-cipher frame.

    :param str plain_text: the plain DSMR telegram ('/...!XXXX\\r\\n')
    :param str encryption_key: hex encryption key
    :param str authentication_key: hex authentication key
    :rtype: bytes
    """
    security_control = SecurityControlField(
        security_suite=security_suite, authenticated=authenticated, encrypted=encrypted
    )
    ciphered = encrypt(
        security_control=security_control,
        key=unhexlify(encryption_key),
        auth_key=unhexlify(authentication_key),
        system_title=system_title,
        invocation_counter=invocation_counter,
        plain_text=plain_text.encode("ascii"),
    )

    security_control_bytes = security_control.to_bytes()
    invocation_counter_bytes = invocation_counter.to_bytes(4, "big")

    frame = bytearray()
    frame.append(GeneralGlobalCipher.TAG)  # 0xDB
    frame.append(len(system_title))
    frame.extend(system_title)
    frame.append(0x82)  # long form length indicator: 2 length bytes follow
    frame.extend(
        (len(security_control_bytes) + len(invocation_counter_bytes) + len(ciphered))
        .to_bytes(2, "big")
    )
    frame.extend(security_control_bytes)
    frame.extend(invocation_counter_bytes)
    frame.extend(ciphered)

    return bytes(frame)
