from decimal import Decimal

import datetime
import json
import unittest

import pytz

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject, MBusObjectPeak
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_FLUVIUS_V171, TELEGRAM_FLUVIUS_V171_ALT


class TelegramParserFluviusTest(unittest.TestCase):
    """ Test parsing of a DSMR Fluvius telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
        try:
            result = parser.parse(TELEGRAM_FLUVIUS_V171, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"

        # BELGIUM_VERSION_INFORMATION (0-0:96.1.4)
        assert isinstance(result.BELGIUM_VERSION_INFORMATION, CosemObject)
        assert result.BELGIUM_VERSION_INFORMATION.unit is None
        assert isinstance(result.BELGIUM_VERSION_INFORMATION.value, str)
        assert result.BELGIUM_VERSION_INFORMATION.value == '50217'

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(result.BELGIUM_EQUIPMENT_IDENTIFIER, CosemObject)
        assert result.BELGIUM_EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(result.BELGIUM_EQUIPMENT_IDENTIFIER.value, str)
        assert result.BELGIUM_EQUIPMENT_IDENTIFIER.value == '3153414733313031303231363035'

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(result.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert result.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(result.P1_MESSAGE_TIMESTAMP.value, datetime.datetime)
        assert result.P1_MESSAGE_TIMESTAMP.value == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 5, 12, 13, 54, 9))

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert result.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert result.ELECTRICITY_USED_TARIFF_1.value == Decimal('0.034')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert result.ELECTRICITY_USED_TARIFF_2.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert result.ELECTRICITY_USED_TARIFF_2.value == Decimal('15.758')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(result.ELECTRICITY_DELIVERED_TARIFF_1, CosemObject)
        assert result.ELECTRICITY_DELIVERED_TARIFF_1.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_DELIVERED_TARIFF_1.value, Decimal)
        assert result.ELECTRICITY_DELIVERED_TARIFF_1.value == Decimal('0.000')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(result.ELECTRICITY_DELIVERED_TARIFF_2, CosemObject)
        assert result.ELECTRICITY_DELIVERED_TARIFF_2.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_DELIVERED_TARIFF_2.value, Decimal)
        assert result.ELECTRICITY_DELIVERED_TARIFF_2.value == Decimal('0.011')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(result.ELECTRICITY_ACTIVE_TARIFF, CosemObject)
        assert result.ELECTRICITY_ACTIVE_TARIFF.unit is None
        assert isinstance(result.ELECTRICITY_ACTIVE_TARIFF.value, str)
        assert result.ELECTRICITY_ACTIVE_TARIFF.value == '0001'

        # BELGIUM_CURRENT_AVERAGE_DEMAND (1-0:1.4.0)
        assert isinstance(result.BELGIUM_CURRENT_AVERAGE_DEMAND, CosemObject)
        assert result.BELGIUM_CURRENT_AVERAGE_DEMAND.unit == 'kW'
        assert isinstance(result.BELGIUM_CURRENT_AVERAGE_DEMAND.value, Decimal)
        assert result.BELGIUM_CURRENT_AVERAGE_DEMAND.value == Decimal('2.351')

        # BELGIUM_MAXIMUM_DEMAND_MONTH (1-0:1.6.0)
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_MONTH, MBusObject)
        assert result.BELGIUM_MAXIMUM_DEMAND_MONTH.unit == 'kW'
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_MONTH.value, Decimal)
        assert result.BELGIUM_MAXIMUM_DEMAND_MONTH.value == Decimal('2.589')
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_MONTH.datetime, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_MONTH.datetime == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 5, 9, 13, 45, 58))

        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 0
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0], MBusObjectPeak)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].unit == 'kW'
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].value, Decimal)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].value == Decimal('3.695')
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].datetime, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].datetime == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 5, 1, 0, 0, 0))
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].occurred, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[0].occurred == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 4, 23, 19, 25, 38))
        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 1
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1], MBusObjectPeak)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].unit == 'kW'
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].value, Decimal)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].value == Decimal('5.980')
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].datetime, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].datetime == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 4, 1, 0, 0, 0))
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].occurred, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[1].occurred == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 3, 5, 12, 21, 39))
        # BELGIUM_MAXIMUM_DEMAND_13_MONTHS (0-0:98.1.0) Value 2
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2], MBusObjectPeak)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].unit == 'kW'
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].value, Decimal)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].value == Decimal('4.318')
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].datetime, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].datetime == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 3, 1, 0, 0, 0))
        assert isinstance(result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].occurred, datetime.datetime)
        assert result.BELGIUM_MAXIMUM_DEMAND_13_MONTHS[2].occurred == \
            pytz.timezone("Europe/Brussels").localize(datetime.datetime(2020, 2, 10, 3, 54, 21))

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert result.CURRENT_ELECTRICITY_USAGE.unit == 'kW'
        assert isinstance(result.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert result.CURRENT_ELECTRICITY_USAGE.value == Decimal('0.000')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert result.CURRENT_ELECTRICITY_DELIVERY.unit == 'kW'
        assert isinstance(result.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert result.CURRENT_ELECTRICITY_DELIVERY.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value == Decimal('0.000')

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L1, CosemObject)
        assert result.INSTANTANEOUS_VOLTAGE_L1.unit == 'V'
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L1.value, Decimal)
        assert result.INSTANTANEOUS_VOLTAGE_L1.value == Decimal('234.7')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L2, CosemObject)
        assert result.INSTANTANEOUS_VOLTAGE_L2.unit == 'V'
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L2.value, Decimal)
        assert result.INSTANTANEOUS_VOLTAGE_L2.value == Decimal('234.7')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L3, CosemObject)
        assert result.INSTANTANEOUS_VOLTAGE_L3.unit == 'V'
        assert isinstance(result.INSTANTANEOUS_VOLTAGE_L3.value, Decimal)
        assert result.INSTANTANEOUS_VOLTAGE_L3.value == Decimal('234.7')

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(result.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert result.INSTANTANEOUS_CURRENT_L1.unit == 'A'
        assert isinstance(result.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert result.INSTANTANEOUS_CURRENT_L1.value == Decimal('0.000')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(result.INSTANTANEOUS_CURRENT_L2, CosemObject)
        assert result.INSTANTANEOUS_CURRENT_L2.unit == 'A'
        assert isinstance(result.INSTANTANEOUS_CURRENT_L2.value, Decimal)
        assert result.INSTANTANEOUS_CURRENT_L2.value == Decimal('0.000')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(result.INSTANTANEOUS_CURRENT_L3, CosemObject)
        assert result.INSTANTANEOUS_CURRENT_L3.unit == 'A'
        assert isinstance(result.INSTANTANEOUS_CURRENT_L3.value, Decimal)
        assert result.INSTANTANEOUS_CURRENT_L3.value == Decimal('0.000')

        # ACTUAL_SWITCH_POSITION (0-0:96.3.10)
        assert isinstance(result.ACTUAL_SWITCH_POSITION, CosemObject)
        assert result.ACTUAL_SWITCH_POSITION.unit is None
        assert isinstance(result.ACTUAL_SWITCH_POSITION.value, int)
        assert result.ACTUAL_SWITCH_POSITION.value == 1

        # ACTUAL_TRESHOLD_ELECTRICITY (0-0:17.0.0)
        assert isinstance(result.ACTUAL_TRESHOLD_ELECTRICITY, CosemObject)
        assert result.ACTUAL_TRESHOLD_ELECTRICITY.unit == 'kW'
        assert isinstance(result.ACTUAL_TRESHOLD_ELECTRICITY.value, Decimal)
        assert result.ACTUAL_TRESHOLD_ELECTRICITY.value == Decimal('999.9')

        # FUSE_THRESHOLD_L1 (1-0:31.4.0)
        assert isinstance(result.FUSE_THRESHOLD_L1, CosemObject)
        assert result.FUSE_THRESHOLD_L1.unit == 'A'
        assert isinstance(result.FUSE_THRESHOLD_L1.value, Decimal)
        assert result.FUSE_THRESHOLD_L1.value == Decimal('999')

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(result.TEXT_MESSAGE, CosemObject)
        assert result.TEXT_MESSAGE.unit is None
        assert result.TEXT_MESSAGE.value is None

        # MBUS DEVICE 1
        mbus1 = result.get_mbus_device_by_channel(1)

        # MBUS_DEVICE_TYPE (0-1:24.1.0)
        assert isinstance(mbus1.MBUS_DEVICE_TYPE, CosemObject)
        assert mbus1.MBUS_DEVICE_TYPE.unit is None
        assert isinstance(mbus1.MBUS_DEVICE_TYPE.value, int)
        assert mbus1.MBUS_DEVICE_TYPE.value == 3

        # MBUS_EQUIPMENT_IDENTIFIER (0-1:96.1.1)
        assert isinstance(mbus1.MBUS_EQUIPMENT_IDENTIFIER, CosemObject)
        assert mbus1.MBUS_EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(mbus1.MBUS_EQUIPMENT_IDENTIFIER.value, str)
        assert mbus1.MBUS_EQUIPMENT_IDENTIFIER.value == '37464C4F32313139303333373333'

        # MBUS_VALVE_POSITION (0-1:24.4.0)
        assert isinstance(result.MBUS_VALVE_POSITION, CosemObject)
        assert result.MBUS_VALVE_POSITION.unit is None
        assert isinstance(result.MBUS_VALVE_POSITION.value, int)
        assert result.MBUS_VALVE_POSITION.value == 1

        # MBUS_METER_READING (0-1:24.2.3)
        assert isinstance(mbus1.MBUS_METER_READING, MBusObject)
        assert mbus1.MBUS_METER_READING.unit == 'm3'
        assert isinstance(mbus1.MBUS_METER_READING.value, Decimal)
        assert mbus1.MBUS_METER_READING.value == Decimal('112.384')

        # MBUS DEVICE 2
        mbus2 = result.get_mbus_device_by_channel(2)

        # MBUS_DEVICE_TYPE (0-2:24.1.0)
        assert isinstance(mbus2.MBUS_DEVICE_TYPE, CosemObject)
        assert mbus2.MBUS_DEVICE_TYPE.unit is None
        assert isinstance(mbus2.MBUS_DEVICE_TYPE.value, int)
        assert mbus2.MBUS_DEVICE_TYPE.value == 7

        # MBUS_EQUIPMENT_IDENTIFIER (0-2:96.1.1)
        assert isinstance(mbus2.MBUS_EQUIPMENT_IDENTIFIER, CosemObject)
        assert mbus2.MBUS_EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(mbus2.MBUS_EQUIPMENT_IDENTIFIER.value, str)
        assert mbus2.MBUS_EQUIPMENT_IDENTIFIER.value == '3853414731323334353637383930'

        # MBUS_METER_READING (0-1:24.2.1)
        assert isinstance(mbus2.MBUS_METER_READING, MBusObject)
        assert mbus2.MBUS_METER_READING.unit == 'm3'
        assert isinstance(mbus2.MBUS_METER_READING.value, Decimal)
        assert mbus2.MBUS_METER_READING.value == Decimal('872.234')

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
        corrupted_telegram = TELEGRAM_FLUVIUS_V171.replace('!3AD7\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_to_json(self):
        parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
        telegram = parser.parse(TELEGRAM_FLUVIUS_V171_ALT)
        json_data = json.loads(telegram.to_json())

        self.maxDiff = None

        self.assertEqual(
            json_data,
            {'BELGIUM_VERSION_INFORMATION': {'value': '50217', 'unit': None},
             'BELGIUM_EQUIPMENT_IDENTIFIER': {'value': '3153414733313030373231333236', 'unit': None},
             'P1_MESSAGE_TIMESTAMP': {'value': '2023-11-02T11:15:48+00:00', 'unit': None},
             'ELECTRICITY_USED_TARIFF_1': {'value': 301.548, 'unit': 'kWh'},
             'ELECTRICITY_USED_TARIFF_2': {'value': 270.014, 'unit': 'kWh'},
             'ELECTRICITY_DELIVERED_TARIFF_1': {'value': 0.005, 'unit': 'kWh'},
             'ELECTRICITY_DELIVERED_TARIFF_2': {'value': 0.0, 'unit': 'kWh'},
             'ELECTRICITY_ACTIVE_TARIFF': {'value': '0001', 'unit': None},
             'BELGIUM_CURRENT_AVERAGE_DEMAND': {'value': 0.052, 'unit': 'kW'},
             'BELGIUM_MAXIMUM_DEMAND_MONTH': {'datetime': '2023-11-02T10:45:00+00:00',
                                              'value': 3.064, 'unit': 'kW'},
             'BELGIUM_MAXIMUM_DEMAND_13_MONTHS': [{'datetime': '2023-07-31T22:00:00+00:00',
                                                   'occurred': None, 'value': 0.0, 'unit': 'kW'},
                                                  {'datetime': '2023-08-31T22:00:00+00:00',
                                                   'occurred': '2023-08-31T16:15:00+00:00',
                                                   'value': 1.862, 'unit': 'kW'},
                                                  {'datetime': '2023-09-30T22:00:00+00:00',
                                                   'occurred': '2023-09-10T16:30:00+00:00',
                                                   'value': 4.229, 'unit': 'kW'},
                                                  {'datetime': '2023-10-31T23:00:00+00:00',
                                                   'occurred': '2023-10-16T11:00:00+00:00',
                                                   'value': 4.927, 'unit': 'kW'}],
             'CURRENT_ELECTRICITY_USAGE': {'value': 0.338, 'unit': 'kW'},
             'CURRENT_ELECTRICITY_DELIVERY': {'value': 0.0, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE': {'value': 0.047, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE': {'value': 0.179, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE': {'value': 0.111, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE': {'value': 0.0, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE': {'value': 0.0, 'unit': 'kW'},
             'INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE': {'value': 0.0, 'unit': 'kW'},
             'INSTANTANEOUS_VOLTAGE_L1': {'value': 232.9, 'unit': 'V'},
             'INSTANTANEOUS_VOLTAGE_L2': {'value': 228.1, 'unit': 'V'},
             'INSTANTANEOUS_VOLTAGE_L3': {'value': 228.1, 'unit': 'V'},
             'INSTANTANEOUS_CURRENT_L1': {'value': 0.27, 'unit': 'A'},
             'INSTANTANEOUS_CURRENT_L2': {'value': 0.88, 'unit': 'A'},
             'INSTANTANEOUS_CURRENT_L3': {'value': 0.52, 'unit': 'A'},
             'ACTUAL_SWITCH_POSITION': {'value': 1, 'unit': None},
             'ACTUAL_TRESHOLD_ELECTRICITY': {'value': 999.9, 'unit': 'kW'},
             'FUSE_THRESHOLD_L1': {'value': 999.0, 'unit': 'A'},
             'TEXT_MESSAGE': {'value': None, 'unit': None},
             'MBUS_DEVICES': [{'MBUS_DEVICE_TYPE': {'value': 3, 'unit': None},
                               'MBUS_EQUIPMENT_IDENTIFIER': {'value': '37464C4F32313233303838303237',
                                                                      'unit': None},
                               'MBUS_VALVE_POSITION': {'value': 1, 'unit': None},
                               'MBUS_METER_READING': {'datetime': '2023-11-02T11:10:02+00:00',
                                                                  'value': 92.287, 'unit': 'm3'},
                               'CHANNEL_ID': 1},
                              {'MBUS_DEVICE_TYPE': {'value': 7, 'unit': None},
                               'MBUS_EQUIPMENT_IDENTIFIER': {'value': '3853455430303030393631313733',
                                                                      'unit': None},
                               'MBUS_METER_READING': {'datetime': '2023-11-02T11:15:32+00:00',
                                                                  'value': 8.579, 'unit': 'm3'},
                               'CHANNEL_ID': 2}]}
        )

    def test_to_str(self):
        parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
        telegram = parser.parse(TELEGRAM_FLUVIUS_V171_ALT)

        self.assertEqual(
            str(telegram),
            (
                'BELGIUM_VERSION_INFORMATION: 	 50217	[None]\n'
                'BELGIUM_EQUIPMENT_IDENTIFIER: 	 3153414733313030373231333236	[None]\n'
                'P1_MESSAGE_TIMESTAMP: 	 2023-11-02T11:15:48+00:00	[None]\n'
                'ELECTRICITY_USED_TARIFF_1: 	 301.548	[kWh]\n'
                'ELECTRICITY_USED_TARIFF_2: 	 270.014	[kWh]\n'
                'ELECTRICITY_DELIVERED_TARIFF_1: 	 0.005	[kWh]\n'
                'ELECTRICITY_DELIVERED_TARIFF_2: 	 0.000	[kWh]\n'
                'ELECTRICITY_ACTIVE_TARIFF: 	 0001	[None]\n'
                'BELGIUM_CURRENT_AVERAGE_DEMAND: 	 0.052	[kW]\n'
                'BELGIUM_MAXIMUM_DEMAND_MONTH: 	 3.064	[kW] at 2023-11-02T10:45:00+00:00\n'
                '0.0	[kW] at 2023-07-31T22:00:00+00:00 occurred None'
                '1.862	[kW] at 2023-08-31T22:00:00+00:00 occurred 2023-08-31T16:15:00+00:00'
                '4.229	[kW] at 2023-09-30T22:00:00+00:00 occurred 2023-09-10T16:30:00+00:00'
                '4.927	[kW] at 2023-10-31T23:00:00+00:00 occurred 2023-10-16T11:00:00+00:00'
                'CURRENT_ELECTRICITY_USAGE: 	 0.338	[kW]\n'
                'CURRENT_ELECTRICITY_DELIVERY: 	 0.000	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE: 	 0.047	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE: 	 0.179	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE: 	 0.111	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE: 	 0.000	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE: 	 0.000	[kW]\n'
                'INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE: 	 0.000	[kW]\n'
                'INSTANTANEOUS_VOLTAGE_L1: 	 232.9	[V]\n'
                'INSTANTANEOUS_VOLTAGE_L2: 	 228.1	[V]\n'
                'INSTANTANEOUS_VOLTAGE_L3: 	 228.1	[V]\n'
                'INSTANTANEOUS_CURRENT_L1: 	 0.27	[A]\n'
                'INSTANTANEOUS_CURRENT_L2: 	 0.88	[A]\n'
                'INSTANTANEOUS_CURRENT_L3: 	 0.52	[A]\n'
                'ACTUAL_SWITCH_POSITION: 	 1	[None]\n'
                'ACTUAL_TRESHOLD_ELECTRICITY: 	 999.9	[kW]\n'
                'FUSE_THRESHOLD_L1: 	 999	[A]\n'
                'TEXT_MESSAGE: 	 None	[None]\n'
                'MBUS DEVICE (channel 1)\n'
                '	MBUS_DEVICE_TYPE: 	 3	[None]\n'
                '	MBUS_EQUIPMENT_IDENTIFIER: 	 37464C4F32313233303838303237	[None]\n'
                '	MBUS_VALVE_POSITION: 	 1	[None]\n'
                '	MBUS_METER_READING: 	 92.287	[m3] at 2023-11-02T11:10:02+00:00\n'
                'MBUS DEVICE (channel 2)\n'
                '	MBUS_DEVICE_TYPE: 	 7	[None]\n'
                '	MBUS_EQUIPMENT_IDENTIFIER: 	 3853455430303030393631313733	[None]\n'
                '	MBUS_METER_READING: 	 8.579	[m3] at 2023-11-02T11:15:32+00:00\n'
            )
        )
