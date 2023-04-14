import unittest

from decimal import Decimal

from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser
from dsmr_parser import telegram_specifications
from dsmr_parser import obis_references as obis
from test.example_telegrams import TELEGRAM_ISKRA_IE


class TelegramParserIskraIETest(unittest.TestCase):
    """ Test parsing of a Iskra IE5 telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.ISKRA_IE)
        try:
            result = parser.parse(TELEGRAM_ISKRA_IE, throw_ex=True)
        except Exception as ex:
            assert False, f"parse trigged an exception {ex}"

        # EQUIPMENT_IDENTIFIER_GAS (0-0:96.1.0)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].value == '09610'

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].value == Decimal('10.181')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].value == Decimal('10.182')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value == Decimal('10.281')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value == Decimal('10.282')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF], CosemObject)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].unit is None
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF].value, str)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].value == '0001'

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].value == Decimal('0.170')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].value == Decimal('0.270')

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value == Decimal('0.217')

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value == Decimal('0.417')

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value == Decimal('0.617')

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value == Decimal('0.227')

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value == Decimal('0.427')

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE], CosemObject)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].unit == 'kW'
        assert isinstance(result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value, Decimal)
        assert result[obis.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value == Decimal('0.627')

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L1], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L1].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L1].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L1].value == Decimal('242.5')

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L2], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L2].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L2].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L2].value == Decimal('241.7')

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L3], CosemObject)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L3].unit == 'V'
        assert isinstance(result[obis.INSTANTANEOUS_VOLTAGE_L3].value, Decimal)
        assert result[obis.INSTANTANEOUS_VOLTAGE_L3].value == Decimal('243.3')

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
        assert isinstance(result[obis.ACTUAL_SWITCH_POSITION].value, str)
        assert result[obis.ACTUAL_SWITCH_POSITION].value == '1'

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.TEXT_MESSAGE].unit is None
        assert result[obis.TEXT_MESSAGE].value is None

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER].unit is None
        assert result[obis.EQUIPMENT_IDENTIFIER].value is None

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_ISKRA_IE)

    def test_checksum_invalid(self):
        # Remove the electricty used data value. This causes the checksum to not match anymore.
        corrupted_telegram = TELEGRAM_ISKRA_IE.replace(
            '1-0:1.8.1(000010.181*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)

    def test_checksum_missing(self):
        # Remove the checksum value causing a ParseError.
        corrupted_telegram = TELEGRAM_ISKRA_IE.replace('!AD3B\r\n', '')
        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted_telegram)
