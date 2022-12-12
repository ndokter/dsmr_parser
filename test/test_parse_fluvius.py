from decimal import Decimal

import datetime
import unittest

import pytz

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject, MBusObjectPeak
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_FLUVIUS_V171


class TelegramParserFluviusTest(unittest.TestCase):
    """ Test parsing of a DSMR Fluvius telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
        result = parser.parse(TELEGRAM_FLUVIUS_V171)

        # BELGIUM_VERSION_INFORMATION (0-0:96.1.4)
        assert isinstance(result[obis.BELGIUM_VERSION_INFORMATION], CosemObject)
        assert result[obis.BELGIUM_VERSION_INFORMATION].unit is None
        assert isinstance(result[obis.BELGIUM_VERSION_INFORMATION].value, str)
        assert result[obis.BELGIUM_VERSION_INFORMATION].value == '50217'

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER].value == '3153414733313031303231363035'

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(result[obis.P1_MESSAGE_TIMESTAMP], CosemObject)
        assert result[obis.P1_MESSAGE_TIMESTAMP].unit is None
        assert isinstance(result[obis.P1_MESSAGE_TIMESTAMP].value, datetime.datetime)
        assert result[obis.P1_MESSAGE_TIMESTAMP].value == \
            datetime.datetime(2020, 5, 12, 11, 54, 9, tzinfo=pytz.UTC)

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].value == Decimal('0.034')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].value == Decimal('15.758')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value == Decimal('0.000')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value == Decimal('0.011')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF], CosemObject)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].unit is None
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF].value, str)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].value == '0001'

        # BELGIUM_CURRENT_AVERAGE_DEMAND (1-0:1.4.0)
        assert isinstance(result[obis.BELGIUM_CURRENT_AVERAGE_DEMAND], CosemObject)
        assert result[obis.BELGIUM_CURRENT_AVERAGE_DEMAND].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_CURRENT_AVERAGE_DEMAND].value, Decimal)
        assert result[obis.BELGIUM_CURRENT_AVERAGE_DEMAND].value == Decimal('2.351')

        # BELGIUM_MAXIMUM_DEMAND_MONTH (1-0:1.6.0)
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_MONTH], MBusObject)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_MONTH].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_MONTH].value, Decimal)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_MONTH].value == Decimal('2.589')

        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 0
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][0], MBusObjectPeak)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][0].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][0].value, Decimal)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][0].value == Decimal('3.695')
        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 1
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][1], MBusObjectPeak)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][1].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][1].value, Decimal)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][1].value == Decimal('5.980')
        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 2
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][2], MBusObjectPeak)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][2].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][2].value, Decimal)
        assert result[obis.BELGIUM_MAXIMUM_DEMAND_13_MONTHS][2].value == Decimal('4.318')

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].value == Decimal('0.000')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value == Decimal('0.000')

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L1], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L1].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L1].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L1].value == Decimal('234.7')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L2], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L2].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L2].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L2].value == Decimal('234.7')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L3], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L3].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L3].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L3].value == Decimal('234.7')

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L1], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L1].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L1].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L1].value == Decimal('0.000')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L2], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L2].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L2].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L2].value == Decimal('0.000')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L3], CosemObject)
        assert result[obis.INSTANTANEOUS_CURRENT_L3].unit == 'A'
        assert isinstance(result[obis.INSTANTANEOUS_CURRENT_L3].value, Decimal)
        assert result[obis.INSTANTANEOUS_CURRENT_L3].value == Decimal('0.000')

        # ACTUAL_SWITCH_POSITION (0-0:96.3.10)
        assert isinstance(result[obis.ACTUAL_SWITCH_POSITION], CosemObject)
        assert result[obis.ACTUAL_SWITCH_POSITION].unit is None
        assert isinstance(result[obis.ACTUAL_SWITCH_POSITION].value, int)
        assert result[obis.ACTUAL_SWITCH_POSITION].value == 1

        # BELGIUM_MAX_POWER_PER_PHASE (0-0:17.0.0)
        assert isinstance(result[obis.BELGIUM_MAX_POWER_PER_PHASE], CosemObject)
        assert result[obis.BELGIUM_MAX_POWER_PER_PHASE].unit == 'kW'
        assert isinstance(result[obis.BELGIUM_MAX_POWER_PER_PHASE].value, Decimal)
        assert result[obis.BELGIUM_MAX_POWER_PER_PHASE].value == Decimal('999.9')

        # BELGIUM_MAX_POWER_PER_PHASE (1-0:31.4.0)
        assert isinstance(result[obis.BELGIUM_MAX_CURRENT_PER_PHASE], CosemObject)
        assert result[obis.BELGIUM_MAX_CURRENT_PER_PHASE].unit == 'A'
        assert isinstance(result[obis.BELGIUM_MAX_CURRENT_PER_PHASE].value, Decimal)
        assert result[obis.BELGIUM_MAX_CURRENT_PER_PHASE].value == Decimal('999')

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.TEXT_MESSAGE].unit is None
        assert result[obis.TEXT_MESSAGE].value is None

        # BELGIUM_MBUS1_DEVICE_TYPE (0-1:24.1.0)
        assert isinstance(result[obis.BELGIUM_MBUS1_DEVICE_TYPE], CosemObject)
        assert result[obis.BELGIUM_MBUS1_DEVICE_TYPE].unit is None
        assert isinstance(result[obis.BELGIUM_MBUS1_DEVICE_TYPE].value, int)
        assert result[obis.BELGIUM_MBUS1_DEVICE_TYPE].value == 3

        # BELGIUM_MBUS1_EQUIPMENT_IDENTIFIER (0-1:96.1.1)
        assert isinstance(result[obis.BELGIUM_MBUS1_EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.BELGIUM_MBUS1_EQUIPMENT_IDENTIFIER].unit is None
        assert isinstance(result[obis.BELGIUM_MBUS1_EQUIPMENT_IDENTIFIER].value, str)
        assert result[obis.BELGIUM_MBUS1_EQUIPMENT_IDENTIFIER].value == '37464C4F32313139303333373333'

        # BELGIUM_MBUS1_VALVE_POSITION (0-1:24.4.0)
        assert isinstance(result[obis.BELGIUM_MBUS1_VALVE_POSITION], CosemObject)
        assert result[obis.BELGIUM_MBUS1_VALVE_POSITION].unit is None
        assert isinstance(result[obis.BELGIUM_MBUS1_VALVE_POSITION].value, int)
        assert result[obis.BELGIUM_MBUS1_VALVE_POSITION].value == 1

        # BELGIUM_MBUS1_METER_READING2 (0-1:24.2.3)
        assert isinstance(result[obis.BELGIUM_MBUS1_METER_READING2], MBusObject)
        assert result[obis.BELGIUM_MBUS1_METER_READING2].unit == 'm3'
        assert isinstance(result[obis.BELGIUM_MBUS1_METER_READING2].value, Decimal)
        assert result[obis.BELGIUM_MBUS1_METER_READING2].value == Decimal('112.384')

        # BELGIUM_MBUS2_DEVICE_TYPE (0-2:24.1.0)
        assert isinstance(result[obis.BELGIUM_MBUS2_DEVICE_TYPE], CosemObject)
        assert result[obis.BELGIUM_MBUS2_DEVICE_TYPE].unit is None
        assert isinstance(result[obis.BELGIUM_MBUS2_DEVICE_TYPE].value, int)
        assert result[obis.BELGIUM_MBUS2_DEVICE_TYPE].value == 7

        # BELGIUM_MBUS2_EQUIPMENT_IDENTIFIER (0-2:96.1.1)
        assert isinstance(result[obis.BELGIUM_MBUS2_EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.BELGIUM_MBUS2_EQUIPMENT_IDENTIFIER].unit is None
        assert isinstance(result[obis.BELGIUM_MBUS2_EQUIPMENT_IDENTIFIER].value, str)
        assert result[obis.BELGIUM_MBUS2_EQUIPMENT_IDENTIFIER].value == '3853414731323334353637383930'

        # BELGIUM_MBUS2_METER_READING1 (0-1:24.2.1)
        assert isinstance(result[obis.BELGIUM_MBUS2_METER_READING1], MBusObject)
        assert result[obis.BELGIUM_MBUS2_METER_READING1].unit == 'm3'
        assert isinstance(result[obis.BELGIUM_MBUS2_METER_READING1].value, Decimal)
        assert result[obis.BELGIUM_MBUS2_METER_READING1].value == Decimal('872.234')


    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_FLUVIUS_V171)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to
        # not match anymore.
        corrupted_telegram = TELEGRAM_FLUVIUS_V171.replace(
            '1-0:1.8.1(000000.034*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_FLUVIUS_V171.replace('!911C\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
