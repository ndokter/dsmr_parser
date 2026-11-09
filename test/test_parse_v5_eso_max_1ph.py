from decimal import Decimal

import datetime
import unittest

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser

from test.example_telegrams import TELEGRAM_V5_ESO_setP1_max_1ph


class TelegramParserV5SetP1Max1PhTest(unittest.TestCase):
    """ Test parsing of DSMR v5 ESO Lithuania setP1 max 1ph telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V5_ESO_LT)

        try:
            telegram = parser.parse(
                TELEGRAM_V5_ESO_setP1_max_1ph,
                throw_ex=True
            )
        except Exception as ex:
            assert False, f"parse triggered an exception {ex}"

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP, CosemObject)
        assert telegram.P1_MESSAGE_TIMESTAMP.unit is None
        assert isinstance(telegram.P1_MESSAGE_TIMESTAMP.value, datetime.datetime)
        assert telegram.P1_MESSAGE_TIMESTAMP.value == \
            datetime.datetime(
                2025,
                6,
                27,
                23,
                14,
                53,
                tzinfo=datetime.timezone.utc
            )

        # ELECTRICITY_IMPORTED_TOTAL (1-0:1.8.0)
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.value == Decimal("721.825")

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_1.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_1.value == Decimal("398.656")

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_2.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_2.value == Decimal("323.169")

        # ELECTRICITY_USED_TARIFF_3 (1-0:1.8.3)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_3.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_3.value == Decimal("0")

        # ELECTRICITY_USED_TARIFF_4 (1-0:1.8.4)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_4.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_4.value == Decimal("0")

        # ELECTRICITY_EXPORTED_TOTAL (1-0:2.8.0)
        assert isinstance(telegram.ELECTRICITY_EXPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_EXPORTED_TOTAL.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_EXPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_EXPORTED_TOTAL.value == Decimal("0")

        # ELECTRICITY_REACTIVE_IMPORTED_TOTAL (1-0:3.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value == Decimal("8.947")

        # ELECTRICITY_REACTIVE_EXPORTED_TOTAL (1-0:4.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value == Decimal("267.426")

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal("0.221")

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal("0")

        # INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE (1-0:23.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value == Decimal("0")

        # INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE (1-0:24.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value == Decimal("0.070")

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.unit == "V"
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.value == Decimal("230.5")

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L1.unit == "A"
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L1.value == 1

        # ESO_LT_FREQUENCY (1-0:14.7.0)
        assert isinstance(telegram.ESO_LT_FREQUENCY, CosemObject)
        assert telegram.ESO_LT_FREQUENCY.unit == "Hz"
        assert isinstance(telegram.ESO_LT_FREQUENCY.value, Decimal)
        assert telegram.ESO_LT_FREQUENCY.value == Decimal("50")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL (1-0:13.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.value == Decimal("0.830")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1 (1-0:33.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.value == Decimal("0.830")

        # SHORT_POWER_FAILURE_COUNT (0-0:96.7.21)
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.SHORT_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT.value, int)
        assert telegram.SHORT_POWER_FAILURE_COUNT.value == 10

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(telegram.TEXT_MESSAGE, CosemObject)
        assert telegram.TEXT_MESSAGE.unit is None
        assert telegram.TEXT_MESSAGE.value == \
            "73657450315F6D61785F317068"

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L1_COUNT.value == 3

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.value == 0

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER, CosemObject)
        assert telegram.EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER.value, str)
        assert telegram.EQUIPMENT_IDENTIFIER.value == "53414731303030303030303030303030"

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(
            TELEGRAM_V5_ESO_setP1_max_1ph
        )

    def test_checksum_invalid(self):
        corrupted = TELEGRAM_V5_ESO_setP1_max_1ph.replace(
            "1-0:1.8.1(000398.656*kWh)\r\n",
            ""
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted)

    def test_checksum_missing(self):
        corrupted = TELEGRAM_V5_ESO_setP1_max_1ph.replace(
            "!BB74\r\n",
            ""
        )

        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted)
