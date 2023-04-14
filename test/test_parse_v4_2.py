from decimal import Decimal
import datetime
import unittest

import pytz

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V4_2


class TelegramParserV4_2Test(unittest.TestCase):
    """ Test parsing of a DSMR v4.2 telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V4)
        try:
            result = parser.parse(TELEGRAM_V4_2, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"

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

        # SHORT_POWER_FAILURE_COUNT (1-0:96.7.21)
        assert isinstance(result[obis.SHORT_POWER_FAILURE_COUNT], CosemObject)
        assert result[obis.SHORT_POWER_FAILURE_COUNT].unit is None
        assert isinstance(result[obis.SHORT_POWER_FAILURE_COUNT].value, int)
        assert result[obis.SHORT_POWER_FAILURE_COUNT].value == 15

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

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L1], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L1].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L1].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L1].value == Decimal('0')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L2], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L2].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L2].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L2].value == Decimal('6')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L3], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L3].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L3].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L3].value == Decimal('2')

        # DEVICE_TYPE (0-x:24.1.0)
        assert isinstance(result[obis.DEVICE_TYPE], CosemObject)
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

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_V4_2)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to
        # not match anymore.
        corrupted_telegram = TELEGRAM_V4_2.replace(
            '1-0:1.8.1(001581.123*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_V4_2.replace('!6796\r\n', '')

        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
