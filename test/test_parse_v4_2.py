from decimal import Decimal
import datetime
import unittest

import pytz

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject
from dsmr_parser.parsers import TelegramParser, TelegramParserV4

TELEGRAM_V4_2 = [
    '/KFM5KAIFA-METER\r\n',
    '\r\n',
    '1-3:0.2.8(42)\r\n',
    '0-0:1.0.0(161113205757W)\r\n',
    '0-0:96.1.1(3960221976967177082151037881335713)\r\n',
    '1-0:1.8.1(001581.123*kWh)\r\n',
    '1-0:1.8.2(001435.706*kWh)\r\n',
    '1-0:2.8.1(000000.000*kWh)\r\n',
    '1-0:2.8.2(000000.000*kWh)\r\n',
    '0-0:96.14.0(0002)\r\n',
    '1-0:1.7.0(02.027*kW)\r\n',
    '1-0:2.7.0(00.000*kW)\r\n',
    '0-0:96.7.21(00015)\r\n',
    '0-0:96.7.9(00007)\r\n',
    '1-0:99.97.0(3)(0-0:96.7.19)(000104180320W)(0000237126*s)(000101000001W)'
    '(2147583646*s)(000102000003W)(2317482647*s)\r\n',
    '1-0:32.32.0(00000)\r\n',
    '1-0:52.32.0(00000)\r\n',
    '1-0:72.32.0(00000)\r\n',
    '1-0:32.36.0(00000)\r\n',
    '1-0:52.36.0(00000)\r\n',
    '1-0:72.36.0(00000)\r\n',
    '0-0:96.13.1()\r\n',
    '0-0:96.13.0()\r\n',
    '1-0:31.7.0(000*A)\r\n',
    '1-0:51.7.0(006*A)\r\n',
    '1-0:71.7.0(002*A)\r\n',
    '1-0:21.7.0(00.170*kW)\r\n',
    '1-0:22.7.0(00.000*kW)\r\n',
    '1-0:41.7.0(01.247*kW)\r\n',
    '1-0:42.7.0(00.000*kW)\r\n',
    '1-0:61.7.0(00.209*kW)\r\n',
    '1-0:62.7.0(00.000*kW)\r\n',
    '0-1:24.1.0(003)\r\n',
    '0-1:96.1.0(4819243993373755377509728609491464)\r\n',
    '0-1:24.2.1(161129200000W)(00981.443*m3)\r\n',
    '!6796\r\n'
]


class TelegramParserV4_2Test(unittest.TestCase):
    """ Test parsing of a DSMR v4.2 telegram. """

    def test_valid(self):
        # No exception is raised.
        TelegramParserV4.validate_telegram_checksum(
            TELEGRAM_V4_2
        )

    def test_invalid(self):
        # Remove one the electricty used data value. This causes the checksum to
        # not match anymore.
        telegram = [line
                    for line in TELEGRAM_V4_2
                    if '1-0:1.8.1' not in line]

        with self.assertRaises(InvalidChecksumError):
            TelegramParserV4.validate_telegram_checksum(telegram)

    def test_missing_checksum(self):
        # Remove the checksum value causing a ParseError.
        telegram = TELEGRAM_V4_2[:-1]

        with self.assertRaises(ParseError):
            TelegramParserV4.validate_telegram_checksum(telegram)

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V4)
        result = parser.parse(TELEGRAM_V4_2)

        # P1_MESSAGE_HEADER (1-3:0.2.8)
        assert isinstance(result[obis.P1_MESSAGE_HEADER], CosemObject)
        assert result[obis.P1_MESSAGE_HEADER].unit is None
        assert isinstance(result[obis.P1_MESSAGE_HEADER].value, str)
        assert result[obis.P1_MESSAGE_HEADER].value == '42'

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(result[obis.P1_MESSAGE_TIMESTAMP], CosemObject)
        assert result[obis.P1_MESSAGE_TIMESTAMP].unit is None
        assert isinstance(result[obis.P1_MESSAGE_TIMESTAMP].value, datetime.datetime)
        assert result[obis.P1_MESSAGE_TIMESTAMP].value == \
            datetime.datetime(2016, 11, 13, 19, 57, 57, tzinfo=pytz.UTC)

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].value == Decimal('1581.123')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].value == Decimal('1435.706')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value == Decimal('0')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value == Decimal('0')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF], CosemObject)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].unit is None
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF].value, str)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].value == '0002'

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER].value == '3960221976967177082151037881335713'

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].value == Decimal('2.027')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].value == Decimal('0')

        # LONG_POWER_FAILURE_COUNT (96.7.9)
        assert isinstance(result[obis.LONG_POWER_FAILURE_COUNT], CosemObject)
        assert result[obis.LONG_POWER_FAILURE_COUNT].unit is None
        assert isinstance(result[obis.LONG_POWER_FAILURE_COUNT].value, int)
        assert result[obis.LONG_POWER_FAILURE_COUNT].value == 7

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(result[obis.VOLTAGE_SAG_L1_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SAG_L1_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SAG_L1_COUNT].value, int)
        assert result[obis.VOLTAGE_SAG_L1_COUNT].value == 0

        # VOLTAGE_SAG_L2_COUNT (1-0:52.32.0)
        assert isinstance(result[obis.VOLTAGE_SAG_L2_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SAG_L2_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SAG_L2_COUNT].value, int)
        assert result[obis.VOLTAGE_SAG_L2_COUNT].value == 0

        # VOLTAGE_SAG_L3_COUNT (1-0:72.32.0)
        assert isinstance(result[obis.VOLTAGE_SAG_L3_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SAG_L3_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SAG_L3_COUNT].value, int)
        assert result[obis.VOLTAGE_SAG_L3_COUNT].value == 0

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        assert isinstance(result[obis.VOLTAGE_SWELL_L1_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SWELL_L1_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SWELL_L1_COUNT].value, int)
        assert result[obis.VOLTAGE_SWELL_L1_COUNT].value == 0

        # VOLTAGE_SWELL_L2_COUNT (1-0:52.36.0)
        assert isinstance(result[obis.VOLTAGE_SWELL_L2_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SWELL_L2_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SWELL_L2_COUNT].value, int)
        assert result[obis.VOLTAGE_SWELL_L2_COUNT].value == 0

        # VOLTAGE_SWELL_L3_COUNT (1-0:72.36.0)
        assert isinstance(result[obis.VOLTAGE_SWELL_L3_COUNT], CosemObject)
        assert result[obis.VOLTAGE_SWELL_L3_COUNT].unit is None
        assert isinstance(result[obis.VOLTAGE_SWELL_L3_COUNT].value, int)
        assert result[obis.VOLTAGE_SWELL_L3_COUNT].value == 0

        # TEXT_MESSAGE_CODE (0-0:96.13.1)
        assert isinstance(result[obis.TEXT_MESSAGE_CODE], CosemObject)
        assert result[obis.TEXT_MESSAGE_CODE].unit is None
        assert result[obis.TEXT_MESSAGE_CODE].value is None

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.TEXT_MESSAGE].unit is None
        assert result[obis.TEXT_MESSAGE].value is None

        # DEVICE_TYPE (0-x:24.1.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.DEVICE_TYPE].unit is None
        assert isinstance(result[obis.DEVICE_TYPE].value, int)
        assert result[obis.DEVICE_TYPE].value == 3

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value == Decimal('0.170')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value == Decimal('1.247')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value == Decimal('0.209')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value == Decimal('0')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value == Decimal('0')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value == Decimal('0')

        # EQUIPMENT_IDENTIFIER_GAS (0-x:96.1.0)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].value == '4819243993373755377509728609491464'

        # HOURLY_GAS_METER_READING (0-1:24.2.1)
        assert isinstance(result[obis.HOURLY_GAS_METER_READING], MBusObject)
        assert result[obis.HOURLY_GAS_METER_READING].unit == 'm3'
        assert isinstance(result[obis.HOURLY_GAS_METER_READING].value, Decimal)
        assert result[obis.HOURLY_GAS_METER_READING].value == Decimal('981.443')

        # POWER_EVENT_FAILURE_LOG (99.97.0)
        # TODO to be implemented

        # ACTUAL_TRESHOLD_ELECTRICITY (0-0:17.0.0)
        # TODO to be implemented

        # ACTUAL_SWITCH_POSITION (0-0:96.3.10)
        # TODO to be implemented

        # VALVE_POSITION_GAS (0-x:24.4.0)
        # TODO to be implemented
