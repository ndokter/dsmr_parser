from unittest.mock import Mock

import unittest

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParser
from dsmr_parser.clients.protocol import create_dsmr_protocol


TELEGRAM_V2_2 = (
    '/ISk5\2MT382-1004\r\n'
    '\r\n'
    '0-0:96.1.1(00000000000000)\r\n'
    '1-0:1.8.1(00001.001*kWh)\r\n'
    '1-0:1.8.2(00001.001*kWh)\r\n'
    '1-0:2.8.1(00001.001*kWh)\r\n'
    '1-0:2.8.2(00001.001*kWh)\r\n'
    '0-0:96.14.0(0001)\r\n'
    '1-0:1.7.0(0001.01*kW)\r\n'
    '1-0:2.7.0(0000.00*kW)\r\n'
    '0-0:17.0.0(0999.00*kW)\r\n'
    '0-0:96.3.10(1)\r\n'
    '0-0:96.13.1()\r\n'
    '0-0:96.13.0()\r\n'
    '0-1:24.1.0(3)\r\n'
    '0-1:96.1.0(000000000000)\r\n'
    '0-1:24.3.0(161107190000)(00)(60)(1)(0-1:24.2.1)(m3)\r\n'
    '(00001.001)\r\n'
    '0-1:24.4.0(1)\r\n'
    '!\r\n'
)


class ProtocolTest(unittest.TestCase):

    def setUp(self):
        new_protocol, _ = create_dsmr_protocol('2.2',
                                               telegram_callback=Mock(),
                                               keep_alive_interval=1)
        self.protocol = new_protocol()

    def test_complete_packet(self):
        """Protocol should assemble incoming lines into complete packet."""

        self.protocol.data_received(TELEGRAM_V2_2.encode('ascii'))

        telegram = self.protocol.telegram_callback.call_args_list[0][0][0]
        assert isinstance(telegram, dict)

        assert float(telegram[obis.CURRENT_ELECTRICITY_USAGE].value) == 1.01
        assert telegram[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'

        assert float(telegram[obis.GAS_METER_READING].value) == 1.001
        assert telegram[obis.GAS_METER_READING].unit == 'm3'

    def test_receive_packet(self):
        """Protocol packet reception."""

        mock_transport = Mock()
        self.protocol.connection_made(mock_transport)
        assert not self.protocol._active

        self.protocol.data_received(TELEGRAM_V2_2.encode('ascii'))
        assert self.protocol._active

        # 1st call of keep_alive resets 'active' flag
        self.protocol.keep_alive()
        assert not self.protocol._active

        # 2nd call of keep_alive should close the transport
        self.protocol.keep_alive()
        assert mock_transport.close.called_once()

        self.protocol.connection_lost(None)
