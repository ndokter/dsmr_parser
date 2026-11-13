import datetime
import unittest
from decimal import Decimal

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject, ProfileGenericObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_SWISS


class TelegramParserSwiss5STest(unittest.TestCase):
    """Test parsing of a Swiss 5S smart meter telegram"""

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.SWISS)
        try:
            telegram = parser.parse(TELEGRAM_SWISS, throw_ex=True)
        except Exception as ex:
            self.fail(f"parse triggered an exception: {ex}")

        # P1_MESSAGE_HEADER (1-3:0.2.8) is not emitted by the Swiss meter.
        assert not hasattr(telegram, 'P1_MESSAGE_HEADER')

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert telegram.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP.value, datetime.datetime)
        assert telegram.P1_MESSAGE_TIMESTAMP.value == \
            datetime.datetime(2024, 9, 18, 12, 12, 28, tzinfo=datetime.timezone.utc)

        # ELECTRICITY_USED_TARIFF_1 (1-1:1.8.1)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_1.value == Decimal('25.600')

        # ELECTRICITY_USED_TARIFF_2 (1-1:1.8.2)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_2.value == Decimal('20.655')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-1:2.8.1)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.value == Decimal('465.932')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-1:2.8.2)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.unit == 'kWh'
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.value == Decimal('3.609')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF, CosemObject)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.unit is None
        assert isinstance(telegram.ELECTRICITY_ACTIVE_TARIFF.value, str)
        assert telegram.ELECTRICITY_ACTIVE_TARIFF.value == '0001'

        # CURRENT_ELECTRICITY_USAGE (1-1:1.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_USAGE.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_USAGE.value == Decimal('0.000')

        # CURRENT_ELECTRICITY_DELIVERY (1-1:2.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.unit == 'kW'
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.value == Decimal('0.006')

        # SHORT_POWER_FAILURE_COUNT (0-0:96.7.21)
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.SHORT_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT.value, int)
        assert telegram.SHORT_POWER_FAILURE_COUNT.value == 9

        # LONG_POWER_FAILURE_COUNT (0-0:96.7.9)
        assert isinstance(telegram.LONG_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.LONG_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.LONG_POWER_FAILURE_COUNT.value, int)
        assert telegram.LONG_POWER_FAILURE_COUNT.value == 8

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L1_COUNT.value == 6

        # VOLTAGE_SAG_L2_COUNT (1-0:52.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L2_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L2_COUNT.value == 1

        # VOLTAGE_SAG_L3_COUNT (1-0:72.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L3_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L3_COUNT.value == 1

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
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.value == Decimal('236.8')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.value == Decimal('239.2')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.unit == 'V'
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.value == Decimal('238.9')

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L1.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L1.value == Decimal('0.70')

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L2.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L2.value == Decimal('1.01')

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L3.unit == 'A'
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L3.value == Decimal('0.51')

        # TEXT_MESSAGE (0-0:96.13.0) - empty in this telegram
        assert isinstance(telegram.TEXT_MESSAGE, CosemObject)
        assert telegram.TEXT_MESSAGE.unit is None
        assert telegram.TEXT_MESSAGE.value is None

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal('0.073')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value == Decimal('0.100')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.unit == 'kW'
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value == Decimal('0.033')

        # POWER_EVENT_FAILURE_LOG (1-0:99.97.0)
        assert isinstance(telegram.POWER_EVENT_FAILURE_LOG, ProfileGenericObject)

        # --- Swiss only ---

        # SWISS_EQUIPMENT_IDENTIFIER (0-0:0.0.0)
        assert isinstance(telegram.SWISS_EQUIPMENT_IDENTIFIER, CosemObject)
        assert telegram.SWISS_EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(telegram.SWISS_EQUIPMENT_IDENTIFIER.value, str)
        assert telegram.SWISS_EQUIPMENT_IDENTIFIER.value == '353738303337'

        # SWISS_VERSION_INFORMATION (0-0:96.1.4)
        assert isinstance(telegram.SWISS_VERSION_INFORMATION, CosemObject)
        assert telegram.SWISS_VERSION_INFORMATION.unit is None
        assert isinstance(telegram.SWISS_VERSION_INFORMATION.value, str)
        assert telegram.SWISS_VERSION_INFORMATION.value == '50220'

        # SWISS_PUBLIC_KEY (0-0:96.1.2)
        assert isinstance(telegram.SWISS_PUBLIC_KEY, CosemObject)
        assert telegram.SWISS_PUBLIC_KEY.unit is None
        assert isinstance(telegram.SWISS_PUBLIC_KEY.value, str)
        assert telegram.SWISS_PUBLIC_KEY.value == (
            '2020202020202020202020202020202020202020202020202020202020'
            '20202020202020202020202020202020202020'
        )

        # SWISS_TEXT_MESSAGE_2 (0-0:96.13.1) - empty in this telegram
        assert isinstance(telegram.SWISS_TEXT_MESSAGE_2, CosemObject)
        assert telegram.SWISS_TEXT_MESSAGE_2.unit is None
        assert telegram.SWISS_TEXT_MESSAGE_2.value is None

        # SWISS_MAXIMUM_DEMAND_MONTH (1-1:1.6.0)
        assert isinstance(telegram.SWISS_MAXIMUM_DEMAND_MONTH, MBusObject)
        assert telegram.SWISS_MAXIMUM_DEMAND_MONTH.unit == 'kW'
        assert isinstance(telegram.SWISS_MAXIMUM_DEMAND_MONTH.value, Decimal)
        assert telegram.SWISS_MAXIMUM_DEMAND_MONTH.value == Decimal('3.468')
        assert isinstance(telegram.SWISS_MAXIMUM_DEMAND_MONTH.datetime, datetime.datetime)
        # 240906083000S -> 2024-09-06 08:30:00 CEST -> 06:30:00 UTC
        assert telegram.SWISS_MAXIMUM_DEMAND_MONTH.datetime == \
            datetime.datetime(2024, 9, 6, 6, 30, 0, tzinfo=datetime.timezone.utc)

        # SWISS_MAXIMUM_DEMAND_MONTHS_COUNT (0-0:98.1.0)
        assert isinstance(telegram.SWISS_MAXIMUM_DEMAND_MONTHS_COUNT, CosemObject)
        assert telegram.SWISS_MAXIMUM_DEMAND_MONTHS_COUNT.unit is None
        assert isinstance(telegram.SWISS_MAXIMUM_DEMAND_MONTHS_COUNT.value, int)
        assert telegram.SWISS_MAXIMUM_DEMAND_MONTHS_COUNT.value == 3

        # SWISS_CURRENT_AVERAGE_DEMAND (1-0:1.4.0)
        assert isinstance(telegram.SWISS_CURRENT_AVERAGE_DEMAND, CosemObject)
        assert telegram.SWISS_CURRENT_AVERAGE_DEMAND.unit == 'kW'
        assert isinstance(telegram.SWISS_CURRENT_AVERAGE_DEMAND.value, Decimal)
        assert telegram.SWISS_CURRENT_AVERAGE_DEMAND.value == Decimal('0.004')

        # No MBus devices in example telegram
        assert not hasattr(telegram, 'MBUS_DEVICES')

    def test_checksum_valid(self):
        TelegramParser.validate_checksum(TELEGRAM_SWISS)

    def test_checksum_invalid(self):
        corrupted_telegram = TELEGRAM_SWISS.replace(
            '1-1:1.8.1(000025.600*kWh)\r\n',
            ''
        )
        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        corrupted_telegram = TELEGRAM_SWISS.replace('!68AA\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
