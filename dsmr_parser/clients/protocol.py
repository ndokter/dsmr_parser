"""Asyncio protocol implementation for handling telegrams."""

from functools import partial
import asyncio
import logging

from serial_asyncio import create_serial_connection

from dsmr_parser import telegram_specifications
from dsmr_parser.clients.telegram_buffer import TelegramBuffer
from dsmr_parser.exceptions import ParseError, InvalidChecksumError
from dsmr_parser.parsers import TelegramParser
from dsmr_parser.clients.settings import SERIAL_SETTINGS_V2_2, \
    SERIAL_SETTINGS_V4, SERIAL_SETTINGS_V5


def create_dsmr_protocol(dsmr_version, telegram_callback, loop=None, **kwargs):
    """Creates a DSMR asyncio protocol."""
    protocol = _create_dsmr_protocol(dsmr_version, telegram_callback,
                                     DSMRProtocol, loop, **kwargs)
    return protocol


# pylama noqa - because of "complex" (too long) if-elif-else.
# Match - case might be a solution but it is not available in <3.10
def _create_dsmr_protocol(dsmr_version, telegram_callback, protocol, loop=None, **kwargs): #noqa
    """Creates a DSMR asyncio protocol."""

    if dsmr_version == '2.2':
        specification = telegram_specifications.V2_2
        serial_settings = SERIAL_SETTINGS_V2_2
    elif dsmr_version == '4':
        specification = telegram_specifications.V4
        serial_settings = SERIAL_SETTINGS_V4
    elif dsmr_version == '4+':
        specification = telegram_specifications.V5
        serial_settings = SERIAL_SETTINGS_V4
    elif dsmr_version == '5':
        specification = telegram_specifications.V5
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == '5B':
        specification = telegram_specifications.BELGIUM_FLUVIUS
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == "5L":
        specification = telegram_specifications.LUXEMBOURG_SMARTY
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == "5S":
        specification = telegram_specifications.SWEDEN
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == "Q3D":
        specification = telegram_specifications.Q3D
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == 'ISKRA_IE':
        specification = telegram_specifications.ISKRA_IE
        serial_settings = SERIAL_SETTINGS_V5
    elif dsmr_version == '5EONHU':
        specification = telegram_specifications.EON_HUNGARY
        serial_settings = SERIAL_SETTINGS_V5
    else:
        raise NotImplementedError("No telegram parser found for version: %s",
                                  dsmr_version)

    protocol = partial(protocol, loop, TelegramParser(specification),
                       telegram_callback=telegram_callback, **kwargs)

    return protocol, serial_settings


def create_dsmr_reader(port, dsmr_version, telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol coroutine using serial port."""
    protocol, serial_settings = create_dsmr_protocol(
        dsmr_version, telegram_callback, loop=None)
    serial_settings['url'] = port

    conn = create_serial_connection(loop, protocol, **serial_settings)
    return conn


def create_tcp_dsmr_reader(host, port, dsmr_version,
                           telegram_callback, loop=None,
                           keep_alive_interval=None):
    """Creates a DSMR asyncio protocol coroutine using TCP connection."""
    if not loop:
        loop = asyncio.get_event_loop()
    protocol, _ = create_dsmr_protocol(
        dsmr_version, telegram_callback, loop=loop,
        keep_alive_interval=keep_alive_interval)
    conn = loop.create_connection(protocol, host, port)
    return conn


class DSMRProtocol(asyncio.Protocol):
    """Assemble and handle incoming data into complete DSM telegrams."""

    transport = None
    telegram_callback = None

    def __init__(self, loop, telegram_parser,
                 telegram_callback=None, keep_alive_interval=None):
        """Initialize class."""
        self.loop = loop
        self.log = logging.getLogger(__name__)
        self.telegram_parser = telegram_parser
        # callback to call on complete telegram
        self.telegram_callback = telegram_callback
        # buffer to keep incomplete incoming data
        self.telegram_buffer = TelegramBuffer()
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

        # accept latin-1 (8-bit) on the line, to allow for non-ascii transport or padding
        data = data.decode("latin1")
        self._active = True
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
            parsed_telegram = self.telegram_parser.parse(telegram)
        except InvalidChecksumError as e:
            self.log.warning(str(e))
        except ParseError:
            self.log.exception("failed to parse telegram")
        else:
            self.telegram_callback(parsed_telegram)

    async def wait_closed(self):
        """Wait until connection is closed."""
        await self._closed.wait()
