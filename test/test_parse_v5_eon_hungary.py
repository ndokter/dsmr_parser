from decimal import Decimal

import datetime
import unittest

import pytz

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V5_EON_HU


class TelegramParserV5EONHUTest(unittest.TestCase):
    """ Test parsing of a DSMR v5 EON Hungary telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.EON_HUNGARY)
        try:
            telegram = parser.parse(TELEGRAM_V5_EON_HU, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert telegram.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP.value, datetime.datetime)
        assert telegram.P1_MESSAGE_TIMESTAMP.value == \
            pytz.timezone("Europe/Budapest").localize(datetime.datetime(2023, 7, 24, 15, 7, 30))

        # EON_HU_COSEM_LOGICAL_DEVICE_NAME (0-0:42.0.0)
        assert isinstance(telegram.COSEM_LOGICAL_DEVICE_NAME, CosemObject)
        assert telegram.COSEM_LOGICAL_DEVICE_NAME.unit is None
        assert isinstance(telegram.COSEM_LOGICAL_DEVICE_NAME.value, str)
        assert telegram.COSEM_LOGICAL_DEVICE_NAME.value == '53414733303832323030303032313630'

        # EON_HU_EQUIPMENT_SERIAL_NUMBER (0-0:96.1.0)
        assert isinstance(telegram.EQUIPMENT_SERIAL_NUMBER, CosemObject)
        assert telegram.EQUIPMENT_SERIAL_NUMBER.unit is None
        assert isinstance(telegram.EQUIPMENT_SERIAL_NUMBER.value, str)
        assert telegram.EQUIPMENT_SERIAL_NUMBER.value == '383930303832323030303032313630'

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF, CosemObject)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.unit is None
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF.value, str)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.value == '0001'

        # ACTUAL_SWITCH_POSITION (0-0:96.3.10)
        assert isinstance(telegram.ACTUAL_SWITCH_POSITION, CosemObject)
        assert telegram.ACTUAL_SWITCH_POSITION.unit is None
        assert isinstance(telegram.ACTUAL_SWITCH_POSITION.value, str)
        assert telegram.ACTUAL_SWITCH_POSITION.value == '1'

        # ACTUAL_TRESHOLD_ELECTRICITY (0-0:17.0.0)
        assert isinstance(telegram.ACTUAL_TRESHOLD_ELECTRICITY, CosemObject)
        assert telegram.ACTUAL_TRESHOLD_ELECTRICITY.unit == 'kW'
        assert isinstance(telegram.ACTUAL_TRESHOLD_ELECTRICITY.value, Decimal)
        assert telegram.ACTUAL_TRESHOLD_ELECTRICITY.value == Decimal('90.000')

        # ELECTRICITY_IMPORTED_TOTAL (1-0:1.8.0)
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.value == Decimal('000173.640')

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_1.value == Decimal('000047.719')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_2.value == Decimal('000125.921')

        # EON_HU_ELECTRICITY_USED_TARIFF_3 (1-0:1.8.3)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_3.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_3.value == Decimal('000000.000')

        # EON_HU_ELECTRICITY_USED_TARIFF_4 (1-0:1.8.4)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_4.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_4.value == Decimal('000000.000')

        # ELECTRICITY_EXPORTED_TOTAL (1-0:2.8.0)
        assert isinstance(telegram.ELECTRICITY_EXPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_EXPORTED_TOTAL.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_EXPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_EXPORTED_TOTAL.value == Decimal('000627.177')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.value == Decimal('000401.829')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.value == Decimal('000225.348')

        # EON_HU_ELECTRICITY_DELIVERED_TARIFF_3 (1-0:2.8.3)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_3.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_3.value == Decimal('000000.000')

        # EON_HU_ELECTRICITY_DELIVERED_TARIFF_4 (1-0:2.8.4)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_4.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_4.value == Decimal('000000.000')

        # ELECTRICITY_REACTIVE_IMPORTED_TOTAL (1-0:3.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value == Decimal('000000.123')

        # ELECTRICITY_REACTIVE_EXPORTED_TOTAL (1-0:4.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value == Decimal('000303.131')

        # EON_HU_ELECTRICITY_REACTIVE_TOTAL_Q1 (1-0:5.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q1, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q1.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q1.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q1.value == Decimal('000000.668')

        # EON_HU_ELECTRICITY_REACTIVE_TOTAL_Q2 (1-0:6.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q2, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q2.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q2.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q2.value == Decimal('000000.071')

        # EON_HU_ELECTRICITY_REACTIVE_TOTAL_Q3 (1-0:7.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q3, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q3.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q3.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q3.value == Decimal('000160.487')

        # EON_HU_ELECTRICITY_REACTIVE_TOTAL_Q4 (1-0:8.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q4, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q4.unit == 'kvarh'
        assert isinstance(telegram.ELECTRICITY_REACTIVE_TOTAL_Q4.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_TOTAL_Q4.value == Decimal('000143.346')

        # EON_HU_ELECTRICITY_COMBINED (1-0:15.8.0)
        assert isinstance(telegram.ELECTRICITY_COMBINED, CosemObject)
        assert telegram.ELECTRICITY_COMBINED.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_COMBINED.value, Decimal)
        assert telegram.ELECTRICITY_COMBINED.value == Decimal('000800.817')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:32.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.value == Decimal('240.4')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.value == Decimal('239.1')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.value == Decimal('241.2')

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L1.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L1.value == Decimal('003')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L2.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L2.value == Decimal('004')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L3.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L3.value == Decimal('003')

        # EON_HU_INSTANTANEOUS_POWER_FACTOR_TOTAL (1-0:13.7.0)
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_TOTAL, CosemObject)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_TOTAL.unit is None
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_TOTAL.value, Decimal)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_TOTAL.value == Decimal('4.556')

        # EON_HU_INSTANTANEOUS_POWER_FACTOR_L1 (1-0:33.7.0)
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L1, CosemObject)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L1.unit is None
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L1.value == Decimal('4.591')

        # EON_HU_INSTANTANEOUS_POWER_FACTOR_L2 (1-0:53.7.0)
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L2, CosemObject)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L2.unit is None
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L2.value == Decimal('4.542')

        # EON_HU_INSTANTANEOUS_POWER_FACTOR_L3 (1-0:73.7.0)
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L3, CosemObject)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L3.unit is None
        assert isinstance(telegram.INSTANTANEOUS_POWER_FACTOR_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_POWER_FACTOR_L3.value == Decimal('4.552')

        # EON_HU_FREQUENCY (1-0:14.7.0)
        assert isinstance(telegram.FREQUENCY, CosemObject)
        assert telegram.FREQUENCY.unit == "Hz"
        assert isinstance(telegram.FREQUENCY.value, Decimal)
        assert telegram.FREQUENCY.value == Decimal('50.00')

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_USAGE.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_USAGE.value == Decimal('00.000')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.value == Decimal('02.601')

        # EON_HU_INSTANTANEOUS_REACTIVE_POWER_Q1 (1-0:5.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q1, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q1.unit == 'kvar'
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q1.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q1.value == Decimal('00.000')

        # EON_HU_INSTANTANEOUS_REACTIVE_POWER_Q2 (1-0:6.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q2, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q2.unit == 'kvar'
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q2.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q2.value == Decimal('00.000')

        # EON_HU_INSTANTANEOUS_REACTIVE_POWER_Q3 (1-0:7.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q3, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q3.unit == 'kvar'
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q3.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q3.value == Decimal('00.504')

        # EON_HU_INSTANTANEOUS_REACTIVE_POWER_Q4 (1-0:8.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q4, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q4.unit == 'kvar'
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_Q4.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_Q4.value == Decimal('00.000')

        # FUSE_THRESHOLD_L1 (1-0:31.4.0)
        assert isinstance(telegram.FUSE_THRESHOLD_L1, CosemObject)
        assert telegram.FUSE_THRESHOLD_L1.unit == 'A'
        assert isinstance(telegram.FUSE_THRESHOLD_L1.value, Decimal)
        assert telegram.FUSE_THRESHOLD_L1.value == Decimal('200.00')

        # FUSE_THRESHOLD_L2 (1-0:31.4.0)
        assert isinstance(telegram.FUSE_THRESHOLD_L2, CosemObject)
        assert telegram.FUSE_THRESHOLD_L2.unit == 'A'
        assert isinstance(telegram.FUSE_THRESHOLD_L2.value, Decimal)
        assert telegram.FUSE_THRESHOLD_L2.value == Decimal('200.00')

        # FUSE_THRESHOLD_L3 (1-0:31.4.0)
        assert isinstance(telegram.FUSE_THRESHOLD_L3, CosemObject)
        assert telegram.FUSE_THRESHOLD_L3.unit == 'A'
        assert isinstance(telegram.FUSE_THRESHOLD_L3.value, Decimal)
        assert telegram.FUSE_THRESHOLD_L3.value == Decimal('200.00')

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(telegram.TEXT_MESSAGE, CosemObject)
        assert telegram.TEXT_MESSAGE.unit is None
        assert telegram.TEXT_MESSAGE.value is None

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_V5_EON_HU)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to
        # not match anymore.
        corrupted_telegram = TELEGRAM_V5_EON_HU.replace(
            '1-0:1.8.1(000047.719*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_V5_EON_HU.replace('!99DA\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
