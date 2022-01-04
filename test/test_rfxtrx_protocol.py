from unittest.mock import Mock

import unittest

from dsmr_parser import obis_references as obis
from dsmr_parser.clients.rfxtrx_protocol import create_rfxtrx_dsmr_protocol, PACKETTYPE_DSMR, SUBTYPE_P1


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

OTHER_RF_PACKET = b'\x03\x01\x02\x03'


def encode_telegram_as_RF_packets(telegram):
    data = b''

    for line in telegram.split('\n'):
        packet_data = (line + '\n').encode('ascii')
        packet_header = bytes(bytearray([
            len(packet_data) + 3,  # excluding length byte
            PACKETTYPE_DSMR,
            SUBTYPE_P1,
            0  # seq num (ignored)
        ]))

        data += packet_header + packet_data
        # other RF packets can pass by on the line
        data += OTHER_RF_PACKET

    return data


class RFXtrxProtocolTest(unittest.TestCase):

    def setUp(self):
        new_protocol, _ = create_rfxtrx_dsmr_protocol('2.2',
                                                      telegram_callback=Mock(),
                                                      keep_alive_interval=1)
        self.protocol = new_protocol()

    def test_complete_packet(self):
        """Protocol should assemble incoming lines into complete packet."""

        data = encode_telegram_as_RF_packets(TELEGRAM_V2_2)
        # send data broken up in two parts
        self.protocol.data_received(data[0:200])
        self.protocol.data_received(data[200:])

        telegram = self.protocol.telegram_callback.call_args_list[0][0][0]
        assert isinstance(telegram, dict)

        assert float(telegram[obis.CURRENT_ELECTRICITY_USAGE].value) == 1.01
        assert telegram[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'

        assert float(telegram[obis.GAS_METER_READING].value) == 1.001
        assert telegram[obis.GAS_METER_READING].unit == 'm3'
