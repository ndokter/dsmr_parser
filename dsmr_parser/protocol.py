"""Asyncio protocol implementation for handling telegrams."""

import asyncio
import logging
from functools import partial

from serial_asyncio import create_serial_connection

from . import telegram_specifications
from .exceptions import ParseError
from .parsers import (
    TelegramParserV2_2,
    TelegramParserV4
)
from .serial import (
    SERIAL_SETTINGS_V2_2, SERIAL_SETTINGS_V4,
    is_end_of_telegram,
    is_start_of_telegram
)


def create_dsmr_reader(port, dsmr_version, telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol coroutine."""

    if dsmr_version == '2.2':
        specifications = telegram_specifications.V2_2
        telegram_parser = TelegramParserV2_2
        serial_settings = SERIAL_SETTINGS_V2_2
    elif dsmr_version == '4':
        specifications = telegram_specifications.V4
        telegram_parser = TelegramParserV4
        serial_settings = SERIAL_SETTINGS_V4

    serial_settings['url'] = port

    protocol = partial(DSMRProtocol, loop, telegram_parser(specifications),
                       telegram_callback=telegram_callback)

    conn = create_serial_connection(loop, protocol, **serial_settings)

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
        # buffer to keep incoming telegram lines
        self.telegram = []
        # buffer to keep incomplete incoming data
        self.buffer = ''

    def connection_made(self, transport):
        """Just logging for now."""
        self.transport = transport
        self.log.debug('connected')

    def data_received(self, data):
        """Add incoming data to buffer."""
        data = data.decode()
        self.log.debug('received data: %s', data.strip())
        self.buffer += data
        self.handle_lines()

    def handle_lines(self):
        """Assemble incoming data into single lines."""
        while "\r\n" in self.buffer:
            line, self.buffer = self.buffer.split("\r\n", 1)
            self.log.debug('got line: %s', line)

            # Telegrams need to be complete because the values belong to a
            # particular reading and can also be related to eachother.
            if not self.telegram and not is_start_of_telegram(line):
                continue

            self.telegram.append(line)
            if is_end_of_telegram(line):
                try:
                    parsed_telegram = self.telegram_parser.parse(self.telegram)
                    self.handle_telegram(parsed_telegram)
                except ParseError:
                    self.log.exception("failed to parse telegram")
                self.telegram = []

    def connection_lost(self, exc):
        """Stop when connection is lost."""
        self.log.error('disconnected')

    def handle_telegram(self, telegram):
        """Send off parsed telegram to handling callback."""
        self.log.debug('got telegram: %s', telegram)

        if self.telegram_callback:
            self.telegram_callback(telegram)
