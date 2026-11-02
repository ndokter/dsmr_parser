import unittest

from datetime import datetime, timezone
from decimal import Decimal

from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser
from dsmr_parser import telegram_specifications
from dsmr_parser.value_types import timestamp_in
from test.example_telegrams import TELEGRAM_ESB_IRELAND


class TelegramParserESBIrelandTest(unittest.TestCase):
    """ Test parsing of an ESB Networks (Ireland) telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.ESB_IRELAND)
        try:
            result = parser.parse(TELEGRAM_ESB_IRELAND, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"

        # every object in the specification was found in the telegram
        assert len(result) == len(telegram_specifications.ESB_IRELAND['objects'])

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0), Irish winter time is UTC
        assert isinstance(result.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert result.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(result.P1_MESSAGE_TIMESTAMP.value, datetime)
        assert result.P1_MESSAGE_TIMESTAMP.value == \
            datetime(2026, 11, 2, 15, 18, 41, tzinfo=timezone.utc)

        # ELECTRICITY_IMPORTED_TOTAL (1-0:1.8.0)
        assert isinstance(result.ELECTRICITY_IMPORTED_TOTAL, CosemObject)
        assert result.ELECTRICITY_IMPORTED_TOTAL.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_IMPORTED_TOTAL.value, Decimal)
        assert result.ELECTRICITY_IMPORTED_TOTAL.value == Decimal('1896.754')

        # ELECTRICITY_EXPORTED_TOTAL (1-0:2.8.0)
        assert isinstance(result.ELECTRICITY_EXPORTED_TOTAL, CosemObject)
        assert result.ELECTRICITY_EXPORTED_TOTAL.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_EXPORTED_TOTAL.value, Decimal)
        assert result.ELECTRICITY_EXPORTED_TOTAL.value == Decimal('653.697')

        # ELECTRICITY_REACTIVE_IMPORTED_TOTAL (1-0:3.8.0)
        assert isinstance(result.ELECTRICITY_REACTIVE_IMPORTED_TOTAL, CosemObject)
        assert result.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.unit == 'kvarh'
        assert isinstance(result.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value, Decimal)
        assert result.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value == Decimal('1.721')

        # ELECTRICITY_REACTIVE_EXPORTED_TOTAL (1-0:4.8.0)
        assert isinstance(result.ELECTRICITY_REACTIVE_EXPORTED_TOTAL, CosemObject)
        assert result.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.unit == 'kvarh'
        assert isinstance(result.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value, Decimal)
        assert result.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value == Decimal('2368.604')

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert result.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert result.ELECTRICITY_USED_TARIFF_1.value == Decimal('28590.571')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert result.ELECTRICITY_USED_TARIFF_2.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert result.ELECTRICITY_USED_TARIFF_2.value == Decimal('2857.943')

        # ELECTRICITY_USED_TARIFF_3 (1-0:1.8.3)
        assert isinstance(result.ELECTRICITY_USED_TARIFF_3, CosemObject)
        assert result.ELECTRICITY_USED_TARIFF_3.unit == 'kWh'
        assert isinstance(result.ELECTRICITY_USED_TARIFF_3.value, Decimal)
        assert result.ELECTRICITY_USED_TARIFF_3.value == Decimal('448.240')

        # SHORT_POWER_FAILURE_COUNT (0-0:96.7.21)
        assert isinstance(result.SHORT_POWER_FAILURE_COUNT, CosemObject)
        assert result.SHORT_POWER_FAILURE_COUNT.unit is None
        assert isinstance(result.SHORT_POWER_FAILURE_COUNT.value, int)
        assert result.SHORT_POWER_FAILURE_COUNT.value == 32

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(result.VOLTAGE_SAG_L1_COUNT, CosemObject)
        assert result.VOLTAGE_SAG_L1_COUNT.unit is None
        assert isinstance(result.VOLTAGE_SAG_L1_COUNT.value, int)
        assert result.VOLTAGE_SAG_L1_COUNT.value == 5

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        assert isinstance(result.VOLTAGE_SWELL_L1_COUNT, CosemObject)
        assert result.VOLTAGE_SWELL_L1_COUNT.unit is None
        assert isinstance(result.VOLTAGE_SWELL_L1_COUNT.value, int)
        assert result.VOLTAGE_SWELL_L1_COUNT.value == 3

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(result.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert result.INSTANTANEOUS_CURRENT_L1.unit == 'A'
        assert isinstance(result.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert result.INSTANTANEOUS_CURRENT_L1.value == Decimal('2.5')

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert result.CURRENT_ELECTRICITY_USAGE.unit == 'kW'
        assert isinstance(result.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert result.CURRENT_ELECTRICITY_USAGE.value == Decimal('0.002')

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal('0.002')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert result.CURRENT_ELECTRICITY_DELIVERY.unit == 'kW'
        assert isinstance(result.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert result.CURRENT_ELECTRICITY_DELIVERY.value == Decimal('0.000')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == 'kW'
        assert isinstance(result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert result.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal('0.000')

        # CURRENT_REACTIVE_IMPORTED (1-0:3.7.0)
        assert isinstance(result.CURRENT_REACTIVE_IMPORTED, CosemObject)
        assert result.CURRENT_REACTIVE_IMPORTED.unit == 'kvar'
        assert isinstance(result.CURRENT_REACTIVE_IMPORTED.value, Decimal)
        assert result.CURRENT_REACTIVE_IMPORTED.value == Decimal('0.000')

        # INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE (1-0:23.7.0)
        assert isinstance(result.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert result.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.unit == 'kvar'
        assert isinstance(result.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert result.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value == Decimal('0.000')

        # CURRENT_REACTIVE_EXPORTED (1-0:4.7.0)
        assert isinstance(result.CURRENT_REACTIVE_EXPORTED, CosemObject)
        assert result.CURRENT_REACTIVE_EXPORTED.unit == 'kvar'
        assert isinstance(result.CURRENT_REACTIVE_EXPORTED.value, Decimal)
        assert result.CURRENT_REACTIVE_EXPORTED.value == Decimal('0.502')

        # INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE (1-0:24.7.0)
        assert isinstance(result.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert result.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.unit == 'kvar'
        assert isinstance(result.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert result.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value == Decimal('0.502')

        # COSEM_LOGICAL_DEVICE_NAME (0-0:42.0.0)
        assert isinstance(result.COSEM_LOGICAL_DEVICE_NAME, CosemObject)
        assert result.COSEM_LOGICAL_DEVICE_NAME.unit is None
        assert isinstance(result.COSEM_LOGICAL_DEVICE_NAME.value, str)
        assert result.COSEM_LOGICAL_DEVICE_NAME.value == '53414731323334353637383930313233'

        # ACTUAL_SWITCH_POSITION (0-0:96.3.10)
        assert isinstance(result.ACTUAL_SWITCH_POSITION, CosemObject)
        assert result.ACTUAL_SWITCH_POSITION.unit is None
        assert isinstance(result.ACTUAL_SWITCH_POSITION.value, str)
        assert result.ACTUAL_SWITCH_POSITION.value == '1'

    def test_timestamp_summer(self):
        # Irish summer time (IST) is UTC+1
        assert timestamp_in('Europe/Dublin')('260715120000S') == datetime(2026, 7, 15, 11, 0, 0, tzinfo=timezone.utc)

    def test_timestamp_dst_end_ambiguous_hour(self):
        # 01:30 occurs twice on 25 October 2026, the S/W flag tells them apart
        assert timestamp_in('Europe/Dublin')('261025013000S') == datetime(2026, 10, 25, 0, 30, 0, tzinfo=timezone.utc)
        assert timestamp_in('Europe/Dublin')('261025013000W') == datetime(2026, 10, 25, 1, 30, 0, tzinfo=timezone.utc)

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_ESB_IRELAND)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to not match anymore.
        corrupted_telegram = TELEGRAM_ESB_IRELAND.replace(
            '1-0:1.8.1(00028590.571*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_ESB_IRELAND.replace('!DE84\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
