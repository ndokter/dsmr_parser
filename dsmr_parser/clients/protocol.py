"""Asyncio protocol implementation for handling telegrams."""

from functools import partial
import asyncio
import logging

from serialx import create_serial_connection

from dsmr_parser.dsmr_versions import DSMR_VERSIONS
from dsmr_parser.clients.telegram_buffer import TelegramBuffer, EncryptedTelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError, DecryptionError
from dsmr_parser.parsers import TelegramParser


def create_dsmr_protocol(dsmr_version, telegram_callback, loop=None, **kwargs):
    """Creates a DSMR asyncio protocol."""
    protocol = _create_dsmr_protocol(dsmr_version, telegram_callback,
                                     DSMRProtocol, loop, **kwargs)
    return protocol


def _create_dsmr_protocol(dsmr_version, telegram_callback, protocol, loop=None, **kwargs):  # noqa
    """Creates a DSMR asyncio protocol."""
    if dsmr_version not in DSMR_VERSIONS:
        raise NotImplementedError("No telegram parser found for version: %s",
                                  dsmr_version)

    specification, serial_settings = DSMR_PROTOCOL_MAPPING[dsmr_version]
    protocol = partial(protocol, loop, TelegramParser(specification),
                       telegram_callback=telegram_callback, **kwargs)

    return protocol, serial_settings


def create_dsmr_reader(port, dsmr_version, telegram_callback, loop=None,
                       keep_alive_interval=None,
                       encryption_key="", authentication_key=""):
    """Creates a DSMR asyncio protocol coroutine using serial port.

    The ``port`` may be a local serial device (e.g. ``/dev/ttyUSB0``) or a
    network URL handled by serialx (e.g. ``socket://host:port``). Pass
    ``keep_alive_interval`` to enable the keep-alive watchdog, which detects
    and recovers from half-open network connections that would otherwise stall
    silently.

    Must be called from within a running event loop unless ``loop`` is given.
    """
    if loop is None:
        loop = asyncio.get_running_loop()
    protocol, serial_settings = create_dsmr_protocol(
        dsmr_version, telegram_callback, loop=loop,
        keep_alive_interval=keep_alive_interval,
        encryption_key=encryption_key, authentication_key=authentication_key)
    serial_settings['url'] = port
    serial_settings['low_latency'] = False
    conn = create_serial_connection(loop, protocol, **serial_settings)
    return conn


def create_tcp_dsmr_reader(host, port, dsmr_version,
                           telegram_callback, loop=None,
                           keep_alive_interval=None,
                           encryption_key="", authentication_key=""):
    """Creates a DSMR asyncio protocol coroutine using a TCP connection.

    This is a thin wrapper around :func:`create_dsmr_reader` using a
    ``socket://`` URL; both establish the exact same TCP connection.
    """
    return create_dsmr_reader(
        f'socket://{host}:{port}', dsmr_version, telegram_callback,
        loop=loop, keep_alive_interval=keep_alive_interval,
        encryption_key=encryption_key, authentication_key=authentication_key)


class DSMRProtocol(asyncio.Protocol):
    """Assemble and handle incoming data into complete DSM telegrams."""

    transport = None
    telegram_callback = None

    def __init__(self, loop, telegram_parser,
                 telegram_callback=None, keep_alive_interval=None,
                 encryption_key="", authentication_key=""):
        """Initialize class."""
        self.loop = loop
        self.log = logging.getLogger(__name__)
        self.telegram_parser = telegram_parser
        # callback to call on complete telegram
        self.telegram_callback = telegram_callback
        # keys used to decrypt encrypted (general-global-cipher) telegrams
        self._encryption_key = encryption_key
        self._authentication_key = authentication_key
        self._encrypted = bool(
            telegram_parser.telegram_specification.get("general_global_cipher"))
        # set when a telegram could not be decrypted; a fatal, unrecoverable
        # condition (wrong key) that tears down the connection
        self.decryption_error: DecryptionError | None = None
        # buffer to keep incomplete incoming data
        self.telegram_buffer = \
            EncryptedTelegramBuffer() if self._encrypted else TelegramBuffer()
        # keep a lock until the connection is closed
        self._closed = asyncio.Event()
        self._keep_alive_interval = keep_alive_interval
        self._active = True

    def connection_made(self, transport):
        """Just logging for now."""
        self.transport = transport
        self.log.debug('connected')
        self._active = False
        if self.loop and self._keep_alive_interval:
            self.loop.call_later(self._keep_alive_interval, self.keep_alive)

    def data_received(self, data):
        """Add incoming data to buffer."""
        self._active = True

        if self._encrypted:
            # Encrypted telegrams are binary DLMS frames; buffer the raw bytes.
            self.telegram_buffer.append(data)
            for telegram in self.telegram_buffer.get_all():
                self.handle_telegram(telegram)
            return

        # accept latin-1 (8-bit) on the line, to allow for non-ascii transport or padding
        data = data.decode("latin1")
        self.log.debug('received data: %s', data)
        self.telegram_buffer.append(data)

        for telegram in self.telegram_buffer.get_all():
            # ensure actual telegram is ascii (7-bit) only (ISO 646:1991 IRV required in section 5.5 of IEC 62056-21)
            telegram = telegram.encode("latin1").decode("ascii")
            self.handle_telegram(telegram)

    def keep_alive(self):
        if self._active:
            self.log.debug('keep-alive checked')
            self._active = False
            if self.loop:
                self.loop.call_later(self._keep_alive_interval, self.keep_alive)
        else:
            self.log.warning('keep-alive check failed')
            if self.transport:
                self.transport.close()

    def connection_lost(self, exc):
        """Stop when connection is lost."""
        if exc:
            self.log.exception('disconnected due to exception', exc_info=exc)
        else:
            self.log.info('disconnected because of close/abort.')
        self._closed.set()

    def handle_telegram(self, telegram):
        """Send off parsed telegram to handling callback."""
        self.log.debug('got telegram: %s', telegram)

        try:
            parsed_telegram = self.telegram_parser.parse(
                telegram,
                encryption_key=self._encryption_key,
                authentication_key=self._authentication_key,
            )
        except DecryptionError as e:
            # Unrecoverable: with a configured key every telegram will fail the
            # same way. Record it and tear down the connection instead of
            # spinning on broken telegrams.
            self.log.error("Failed to decrypt telegram, check the keys: %s", e)
            self.decryption_error = e
            if self.transport:
                self.transport.close()
        except InvalidChecksumError as e:
            self.log.info(str(e))
        except ParseError:
            self.log.exception("failed to parse telegram")
        else:
            self.telegram_callback(parsed_telegram)

    async def wait_closed(self):
        """Wait until connection is closed."""
        await self._closed.wait()
