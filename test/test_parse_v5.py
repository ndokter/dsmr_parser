from decimal import Decimal

import datetime
import unittest

import pytz

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V5


class TelegramParserV5Test(unittest.TestCase):
    """ Test parsing of a DSMR v5.x telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V5)
        try:
            telegram = parser.parse(TELEGRAM_V5, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"
        print('test: ', type(telegram.P1_MESSAGE_HEADER), telegram.P1_MESSAGE_HEADER.__dict__)
        # P1_MESSAGE_HEADER (1-3:0.2.8)
        assert isinstance(telegram.P1_MESSAGE_HEADER, CosemObject)
        assert telegram.P1_MESSAGE_HEADER.unit is None
        assert isinstance(telegram.P1_MESSAGE_HEADER.value, str)
        assert telegram.P1_MESSAGE_HEADER.value == '50'

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert telegram.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP.value, datetime.datetime)
        assert telegram.P1_MESSAGE_TIMESTAMP.value == \
            datetime.datetime(2017, 1, 2, 18, 20, 2, tzinfo=pytz.UTC)

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_1.value == Decimal('4.426')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_2.value == Decimal('2.399')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.value == Decimal('2.444')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.value == Decimal('0')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF, CosemObject)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.unit is None
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF.value, str)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.value == '0002'

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER, CosemObject)
        assert telegram.EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER.value, str)
        assert telegram.EQUIPMENT_IDENTIFIER.value == '4B384547303034303436333935353037'

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_USAGE.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_USAGE.value == Decimal('0.244')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.value == Decimal('0')

        # LONG_POWER_FAILURE_COUNT (96.7.9)
        assert isinstance(telegram.LONG_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.LONG_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.LONG_POWER_FAILURE_COUNT.value, int)
        assert telegram.LONG_POWER_FAILURE_COUNT.value == 0

        # SHORT_POWER_FAILURE_COUNT (1-0:96.7.21)
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.SHORT_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT.value, int)
        assert telegram.SHORT_POWER_FAILURE_COUNT.value == 13

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L1_COUNT.value == 0

        # VOLTAGE_SAG_L2_COUNT (1-0:52.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L2_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L2_COUNT.value == 0

        # VOLTAGE_SAG_L3_COUNT (1-0:72.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L3_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L3_COUNT.value == 0

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.value == 0

        # VOLTAGE_SWELL_L2_COUNT (1-0:52.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L2_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L2_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L2_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L2_COUNT.value == 0

        # VOLTAGE_SWELL_L3_COUNT (1-0:72.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L3_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L3_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L3_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L3_COUNT.value == 0

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.value == Decimal('230.0')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.value == Decimal('230.0')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.value == Decimal('229.0')

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L1.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L1.value == Decimal('0.48')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L2.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L2.value == Decimal('0.44')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L3.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L3.value == Decimal('0.86')

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(telegram.TEXT_MESSAGE, CosemObject)
        assert telegram.TEXT_MESSAGE.unit is None
        assert telegram.TEXT_MESSAGE.value is None

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal('0.070')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value == Decimal('0.032')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value == Decimal('0.142')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal('0')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value == Decimal('0')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value == Decimal('0')

        # There's only one Mbus device (gas meter) in this case. Alternatively
        # use get_mbus_device_by_channel
        gas_meter_devices = telegram.MBUS_DEVICES
        gas_meter_device = gas_meter_devices[0]

        # MBUS_DEVICE_TYPE (0-1:96.1.0)
        assert isinstance(gas_meter_device.MBUS_DEVICE_TYPE, CosemObject)
        assert gas_meter_device.MBUS_DEVICE_TYPE.unit is None
        assert isinstance(gas_meter_device.MBUS_DEVICE_TYPE.value, int)
        assert gas_meter_device.MBUS_DEVICE_TYPE.value == 3

        # MBUS_EQUIPMENT_IDENTIFIER (0-1:96.1.0)
        assert isinstance(gas_meter_device.MBUS_EQUIPMENT_IDENTIFIER, CosemObject)
        assert gas_meter_device.MBUS_EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(gas_meter_device.MBUS_EQUIPMENT_IDENTIFIER.value, str)
        assert gas_meter_device.MBUS_EQUIPMENT_IDENTIFIER.value == '3232323241424344313233343536373839'

        # MBUS_METER_READING (0-1:24.2.1)
        assert isinstance(gas_meter_device.MBUS_METER_READING, MBusObject)
        assert gas_meter_device.MBUS_METER_READING.unit == 'm3'
        assert isinstance(telegram.MBUS_METER_READING.value, Decimal)
        assert gas_meter_device.MBUS_METER_READING.value == Decimal('0.107')

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_V5)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to
        # not match anymore.
        corrupted_telegram = TELEGRAM_V5.replace(
            '1-0:1.8.1(000004.426*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_V5.replace('!6EEE\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_gas_timestamp_invalid(self):
        # Issue 120
        # Sometimes a MBUS device (For ex a Gas Meter) returns an invalid timestamp
        # Instead of failing, we should just ignore the timestamp
        invalid_date_telegram = TELEGRAM_V5.replace(
            '0-1:24.2.1(170102161005W)(00000.107*m3)\r\n',
            '0-1:24.2.1(632525252525S)(00000.000)\r\n'
        )
        invalid_date_telegram = invalid_date_telegram.replace('!6EEE\r\n', '!90C2\r\n')
        parser = TelegramParser(telegram_specifications.V5)
        telegram = parser.parse(invalid_date_telegram)

        # MBUS DEVICE 1
        mbus1 = telegram.get_mbus_device_by_channel(1)

        # MBUS_METER_READING (0-1:24.2.1)
        assert isinstance(mbus1.MBUS_METER_READING, MBusObject)
        assert mbus1.MBUS_METER_READING.unit is None
        assert isinstance(mbus1.MBUS_METER_READING.value, Decimal)
        assert mbus1.MBUS_METER_READING.value == Decimal('0.000')
