"""Test telegram parsing."""

from dsmr_parser.parsers import TelegramParserV2_2
from dsmr_parser import telegram_specifications
from dsmr_parser.obis_references import CURRENT_ELECTRICITY_USAGE, GAS_METER_READING

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


def test_parse_v2_2():
    """Test if telegram parsing results in correct results."""

    parser = TelegramParserV2_2(telegram_specifications.V2_2)
    result = parser.parse(TELEGRAM_V2_2)

    assert float(result[CURRENT_ELECTRICITY_USAGE].value) == 1.01
    assert result[CURRENT_ELECTRICITY_USAGE].unit == 'kW'
    assert float(result[GAS_METER_READING].value) == 1.001
    assert result[GAS_METER_READING].unit == 'm3'
