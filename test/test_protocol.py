"""Test DSMR serial protocol."""

from unittest.mock import Mock

import pytest

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParserV2_2
from dsmr_parser.protocol import DSMRProtocol


TELEGRAM_V2_2 = [
    "/ISk5\2MT382-1004",
    "",
    "0-0:96.1.1(00000000000000)",
    "1-0:1.8.1(00001.001*kWh)",
    "1-0:1.8.2(00001.001*kWh)",
    "1-0:2.8.1(00001.001*kWh)",
    "1-0:2.8.2(00001.001*kWh)",
    "0-0:96.14.0(0001)",
    "1-0:1.7.0(0001.01*kW)",
    "1-0:2.7.0(0000.00*kW)",
    "0-0:17.0.0(0999.00*kW)",
    "0-0:96.3.10(1)",
    "0-0:96.13.1()",
    "0-0:96.13.0()",
    "0-1:24.1.0(3)",
    "0-1:96.1.0(000000000000)",
    "0-1:24.3.0(161107190000)(00)(60)(1)(0-1:24.2.1)(m3)",
    "(00001.001)",
    "0-1:24.4.0(1)",
    "!",
]


@pytest.fixture
def protocol():
    """DSMRprotocol instance with mocked telegram_callback."""

    parser = TelegramParserV2_2
    specification = telegram_specifications.V2_2

    telegram_parser = parser(specification)
    return DSMRProtocol(None, telegram_parser,
                        telegram_callback=Mock())


def test_complete_packet(protocol):
    """Protocol should assemble incoming lines into complete packet."""

    for line in TELEGRAM_V2_2:
        protocol.data_received(bytes(line + '\r\n', 'ascii'))

    telegram = protocol.telegram_callback.call_args_list[0][0][0]
    assert isinstance(telegram, dict)

    assert float(telegram[obis.CURRENT_ELECTRICITY_USAGE].value) == 1.01
    assert telegram[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'

    assert float(telegram[obis.GAS_METER_READING].value) == 1.001
    assert telegram[obis.GAS_METER_READING].unit == 'm3'
