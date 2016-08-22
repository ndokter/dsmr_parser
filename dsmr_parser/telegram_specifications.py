from decimal import Decimal

from .obis_references import *
from .parsers import CosemParser, ValueParser, MBusParser
from .value_types import timestamp


"""
dsmr_parser.telegram_specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains DSMR telegram specifications. Each specifications describes
how the telegram lines are parsed.
"""

V4 = {
    P1_MESSAGE_HEADER: CosemParser(ValueParser(str)),
    P1_MESSAGE_TIMESTAMP: CosemParser(ValueParser(timestamp)),
    ELECTRICITY_USED_TARIFF_1: CosemParser(ValueParser(Decimal)),
    ELECTRICITY_USED_TARIFF_2: CosemParser(ValueParser(Decimal)),
    ELECTRICITY_DELIVERED_TARIFF_1: CosemParser(ValueParser(Decimal)),
    ELECTRICITY_DELIVERED_TARIFF_2: CosemParser(ValueParser(Decimal)),
    ELECTRICITY_ACTIVE_TARIFF: CosemParser(ValueParser(str)),
    EQUIPMENT_IDENTIFIER: CosemParser(ValueParser(str)),
    CURRENT_ELECTRICITY_USAGE: CosemParser(ValueParser(Decimal)),
    CURRENT_ELECTRICITY_DELIVERY: CosemParser(ValueParser(Decimal)),
    LONG_POWER_FAILURE_COUNT: CosemParser(ValueParser(int)),
    # POWER_EVENT_FAILURE_LOG: ProfileGenericParser(), TODO
    VOLTAGE_SAG_L1_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SAG_L2_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SAG_L3_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L1_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L2_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L3_COUNT: CosemParser(ValueParser(int)),
    TEXT_MESSAGE_CODE: CosemParser(ValueParser(int)),
    TEXT_MESSAGE: CosemParser(ValueParser(str)),
    DEVICE_TYPE: CosemParser(ValueParser(int)),
    INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE: CosemParser(ValueParser(Decimal)),
    INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE: CosemParser(ValueParser(Decimal)),
    INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE: CosemParser(ValueParser(Decimal)),
    INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE: CosemParser(ValueParser(Decimal)),
    INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE: CosemParser(ValueParser(Decimal)),
    INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE: CosemParser(ValueParser(Decimal)),
    EQUIPMENT_IDENTIFIER_GAS: CosemParser(ValueParser(str)),
    HOURLY_GAS_METER_READING: MBusParser(ValueParser(timestamp),
                                         ValueParser(Decimal))
}

