"""Test DSMR serial protocol."""

from unittest.mock import Mock

import pytest
from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParserV2_2
from dsmr_parser.protocol import DSMRProtocol

from .test_parse_v2_2 import TELEGRAM_V2_2


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
