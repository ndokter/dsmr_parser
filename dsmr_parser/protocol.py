"""Asyncio protocol implementation for handling telegrams."""

import asyncio
import logging
from functools import partial

from serial_asyncio import create_serial_connection

from . import telegram_specifications
from .exceptions import ParseError
from .parsers import TelegramParserV2_2, TelegramParserV4
from .serial import (SERIAL_SETTINGS_V2_2, SERIAL_SETTINGS_V4,
                     is_end_of_telegram, is_start_of_telegram, TelegramBuffer)


def create_dsmr_protocol(dsmr_version, telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol."""

    if dsmr_version == '2.2':
        specifications = telegram_specifications.V2_2
        telegram_parser = TelegramParserV2_2
        serial_settings = SERIAL_SETTINGS_V2_2
    elif dsmr_version == '4':
        specifications = telegram_specifications.V4
        telegram_parser = TelegramParserV4
        serial_settings = SERIAL_SETTINGS_V4
    else:
        raise NotImplementedError("No telegram parser found for version: %s",
                                  dsmr_version)

    protocol = partial(DSMRProtocol, loop, telegram_parser(specifications),
                       telegram_callback=telegram_callback)

    return protocol, serial_settings


def create_dsmr_reader(port, dsmr_version, telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol coroutine using serial port."""
    protocol, serial_settings = create_dsmr_protocol(
        dsmr_version, telegram_callback, loop=None)
    serial_settings['url'] = port

    conn = create_serial_connection(loop, protocol, **serial_settings)
    return conn


def create_tcp_dsmr_reader(host, port, dsmr_version,
                           telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol coroutine using TCP connection."""
    protocol, _ = create_dsmr_protocol(
        dsmr_version, telegram_callback, loop=None)
    conn = loop.create_connection(protocol, host, port)
    return conn


class DSMRProtocol(asyncio.Protocol):
    """Assemble and handle incoming data into complete DSM telegrams."""

    transport = None
    telegram_callback = None

    def __init__(self, loop, telegram_parser, telegram_callback=None):
        """Initialize class."""
        self.loop = loop
        self.log = logging.getLogger(__name__)
        self.telegram_parser = telegram_parser
        # callback to call on complete telegram
        self.telegram_callback = telegram_callback
        # buffer to keep incomplete incoming data
        self.telegram_buffer = TelegramBuffer(self.handle_telegram)
        # keep a lock until the connection is closed
        self._closed = asyncio.Event()

    def connection_made(self, transport):
        """Just logging for now."""
        self.transport = transport
        self.log.debug('connected')

    def data_received(self, data):
        """Add incoming data to buffer."""
        data = data.decode('ascii')
        self.log.debug('received data: %s', data)
        self.telegram_buffer.append(data)

    def connection_lost(self, exc):
        """Stop when connection is lost."""
        if exc:
            self.log.exception('disconnected due to exception')
        else:
            self.log.info('disconnected because of close/abort.')
        self._closed.set()

    def handle_telegram(self, telegram):
        """Send off parsed telegram to handling callback."""
        self.log.debug('got telegram: %s', telegram)

        if self.telegram_callback:
            self.telegram_callback(telegram)

    @asyncio.coroutine
    def wait_closed(self):
        """Wait until connection is closed."""
        yield from self._closed.wait()
