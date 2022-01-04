"""Asyncio protocol implementation for handling telegrams over a RFXtrx connection ."""

import asyncio

from serial_asyncio import create_serial_connection
from .protocol import DSMRProtocol, _create_dsmr_protocol


def create_rfxtrx_dsmr_protocol(dsmr_version, telegram_callback, loop=None, **kwargs):
    """Creates a RFXtrxDSMR asyncio protocol."""
    protocol = _create_dsmr_protocol(dsmr_version, telegram_callback,
                                     RFXtrxDSMRProtocol, loop, **kwargs)
    return protocol


def create_rfxtrx_dsmr_reader(port, dsmr_version, telegram_callback, loop=None):
    """Creates a DSMR asyncio protocol coroutine using a RFXtrx serial port."""
    protocol, serial_settings = create_rfxtrx_dsmr_protocol(
        dsmr_version, telegram_callback, loop=None)
    serial_settings['url'] = port

    conn = create_serial_connection(loop, protocol, **serial_settings)
    return conn


def create_rfxtrx_tcp_dsmr_reader(host, port, dsmr_version,
                                  telegram_callback, loop=None,
                                  keep_alive_interval=None):
    """Creates a DSMR asyncio protocol coroutine using a RFXtrx TCP connection."""
    if not loop:
        loop = asyncio.get_event_loop()
    protocol, _ = create_rfxtrx_dsmr_protocol(
        dsmr_version, telegram_callback, loop=loop,
        keep_alive_interval=keep_alive_interval)
    conn = loop.create_connection(protocol, host, port)
    return conn


PACKETTYPE_DSMR = 0x62
SUBTYPE_P1 = 0x01


class RFXtrxDSMRProtocol(DSMRProtocol):

    remaining_data = b''

    def data_received(self, data):
        """Add incoming data to buffer."""

        data = self.remaining_data + data

        packetlength = data[0] + 1 if len(data) > 0 else 1
        while packetlength <= len(data):
            packettype = data[1]
            subtype = data[2]
            if (packettype == PACKETTYPE_DSMR and subtype == SUBTYPE_P1):
                dsmr_data = data[4:packetlength]
                super().data_received(dsmr_data)
            data = data[packetlength:]
            packetlength = data[0] + 1 if len(data) > 0 else 1

        self.remaining_data = data
