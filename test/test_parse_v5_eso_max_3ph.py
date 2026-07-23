from decimal import Decimal

import datetime
import unittest

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser

from test.example_telegrams import TELEGRAM_V5_ESO_setP1_max_3ph


class TelegramParserV5SetP1Max3PhTest(unittest.TestCase):
    """ Test parsing of DSMR v5 ESO Lithuania setP1 max 3ph telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V5_ESO_LT)

        try:
            telegram = parser.parse(
                TELEGRAM_V5_ESO_setP1_max_3ph,
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
                7,
                12,
                17,
                39,
                49,
                tzinfo=datetime.timezone.utc
            )

        # ELECTRICITY_IMPORTED_TOTAL (1-0:1.8.0)
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_IMPORTED_TOTAL.value == Decimal("7926")

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_1.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_1.value == Decimal("7926")

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_USED_TARIFF_2.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_USED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_USED_TARIFF_2.value == Decimal("0")

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
        assert telegram.ELECTRICITY_EXPORTED_TOTAL.value == Decimal("20183.680")

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_1.value == Decimal("20183.680")

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_2.value == Decimal("0")

        # ELECTRICITY_DELIVERED_TARIFF_3 (1-0:2.8.3)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_3.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_3.value == Decimal("0")

        # ELECTRICITY_DELIVERED_TARIFF_4 (1-0:2.8.4)
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_4.unit == "kWh"
        assert isinstance(telegram.ELECTRICITY_DELIVERED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_DELIVERED_TARIFF_4.value == Decimal("0")

        # ELECTRICITY_REACTIVE_IMPORTED_TOTAL (1-0:3.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TOTAL.value == Decimal("11688.602")

        # ELECTRICITY_REACTIVE_IMPORTED_TARIFF_1 (1-0:3.8.1)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_1.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_1.value == Decimal("11688.602")

        # ELECTRICITY_REACTIVE_IMPORTED_TARIFF_2 (1-0:3.8.2)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_2.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_2.value == Decimal("0")

        # ELECTRICITY_REACTIVE_IMPORTED_TARIFF_3 (1-0:3.8.3)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_3.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_3.value == Decimal("0")

        # ELECTRICITY_REACTIVE_IMPORTED_TARIFF_4 (1-0:3.8.4)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_4.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_IMPORTED_TARIFF_4.value == Decimal("0")

        # ELECTRICITY_REACTIVE_EXPORTED_TOTAL (1-0:4.8.0)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TOTAL.value == Decimal("1050.043")

        # ELECTRICITY_REACTIVE_EXPORTED_TARIFF_1 (1-0:4.8.1)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_1, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_1.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_1.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_1.value == Decimal("1050.043")

        # ELECTRICITY_REACTIVE_EXPORTED_TARIFF_2 (1-0:4.8.2)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_2, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_2.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_2.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_2.value == Decimal("0")

        # ELECTRICITY_REACTIVE_EXPORTED_TARIFF_3 (1-0:4.8.3)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_3, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_3.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_3.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_3.value == Decimal("0")

        # ELECTRICITY_REACTIVE_EXPORTED_TARIFF_4 (1-0:4.8.4)
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_4, CosemObject)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_4.unit == "kvarh"
        assert isinstance(telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_4.value, Decimal)
        assert telegram.ELECTRICITY_REACTIVE_EXPORTED_TARIFF_4.value == Decimal("0")

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_USAGE.unit == "kW"
        assert isinstance(telegram.CURRENT_ELECTRICITY_USAGE.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_USAGE.value == Decimal("0.145")

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY, CosemObject)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.unit == "kW"
        assert isinstance(telegram.CURRENT_ELECTRICITY_DELIVERY.value, Decimal)
        assert telegram.CURRENT_ELECTRICITY_DELIVERY.value == Decimal("0")

        # CURRENT_REACTIVE_IMPORTED (1-0:3.7.0)
        assert isinstance(telegram.CURRENT_REACTIVE_IMPORTED, CosemObject)
        assert telegram.CURRENT_REACTIVE_IMPORTED.unit == "kvar"
        assert isinstance(telegram.CURRENT_REACTIVE_IMPORTED.value, Decimal)
        assert telegram.CURRENT_REACTIVE_IMPORTED.value == Decimal("0")

        # CURRENT_REACTIVE_EXPORTED (1-0:4.7.0)
        assert isinstance(telegram.CURRENT_REACTIVE_EXPORTED, CosemObject)
        assert telegram.CURRENT_REACTIVE_EXPORTED.unit == "kvar"
        assert isinstance(telegram.CURRENT_REACTIVE_EXPORTED.value, Decimal)
        assert telegram.CURRENT_REACTIVE_EXPORTED.value == Decimal("0.061")

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE.value == Decimal("0")

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE.value == Decimal("0")

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE.value == Decimal("1.259")

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE.value == Decimal("0.273")

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE.value == Decimal("0.382")

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.unit == "kW"
        assert isinstance(telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE.value == Decimal("0")

        # INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE (1-0:23.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_POSITIVE.value == Decimal("0.085")

        # INSTANTANEOUS_REACTIVE_POWER_L2_POSITIVE (1-0:43.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L2_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L2_POSITIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L2_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L2_POSITIVE.value == Decimal("0")

        # INSTANTANEOUS_REACTIVE_POWER_L3_POSITIVE (1-0:63.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L3_POSITIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L3_POSITIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L3_POSITIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L3_POSITIVE.value == Decimal("0.156")

        # INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE (1-0:24.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L1_NEGATIVE.value == Decimal("0")

        # INSTANTANEOUS_REACTIVE_POWER_L2_NEGATIVE (1-0:44.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L2_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L2_NEGATIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L2_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L2_NEGATIVE.value == Decimal("0.032")

        # INSTANTANEOUS_REACTIVE_POWER_L3_NEGATIVE (1-0:64.7.0)
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L3_NEGATIVE, CosemObject)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L3_NEGATIVE.unit == "kvar"
        assert isinstance(telegram.INSTANTANEOUS_REACTIVE_POWER_L3_NEGATIVE.value, Decimal)
        assert telegram.INSTANTANEOUS_REACTIVE_POWER_L3_NEGATIVE.value == Decimal("0")

        # INSTANTANEOUS_VOLTAGE_L1 (1-0:32.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.unit == "V"
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L1.value == Decimal("243.0")

        # ESO_LT_AVERAGE_VOLTAGE_L1 (1-0:32.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L1, CosemObject)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L1.unit == "V"
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L1.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L1.value == Decimal("243.0")

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L1.unit == "A"
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L1.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L1.value == 1

        # INSTANTANEOUS_VOLTAGE_L2 (1-0:52.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.unit == "V"
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L2.value == Decimal("243.4")

        # ESO_LT_AVERAGE_VOLTAGE_L2 (1-0:52.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L2, CosemObject)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L2.unit == "V"
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L2.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L2.value == Decimal("242.7")

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L2.unit == "A"
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L2.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L2.value == 1

        # INSTANTANEOUS_VOLTAGE_L3 (1-0:72.7.0)
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3, CosemObject)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.unit == "V"
        assert isinstance(telegram.INSTANTANEOUS_VOLTAGE_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_VOLTAGE_L3.value == Decimal("236.2")

        # ESO_LT_AVERAGE_VOLTAGE_L3 (1-0:72.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L3, CosemObject)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L3.unit == "V"
        assert isinstance(telegram.ESO_LT_AVERAGE_VOLTAGE_L3.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_VOLTAGE_L3.value == Decimal("237.8")

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3, CosemObject)
        assert telegram.INSTANTANEOUS_CURRENT_L3.unit == "A"
        assert isinstance(telegram.INSTANTANEOUS_CURRENT_L3.value, Decimal)
        assert telegram.INSTANTANEOUS_CURRENT_L3.value == 5

        # ESO_LT_INSTANTANEOUS_VOLTAGE (1-0:12.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_VOLTAGE, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_VOLTAGE.unit == "V"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_VOLTAGE.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_VOLTAGE.value == Decimal("243.4")

        # ESO_LT_INSTANTANEOUS_CURRENT (1-0:11.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT.unit == "A"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT.value == 5

        # ESO_LT_INSTANTANEOUS_CURRENT_IN_NEUTRAL (1-0:91.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT_IN_NEUTRAL, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT_IN_NEUTRAL.unit == "A"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT_IN_NEUTRAL.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT_IN_NEUTRAL.value == 0

        # ESO_LT_INSTANTANEOUS_CURRENT_SUM_OVER_ALL_PHASES (1-0:90.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT_SUM_OVER_ALL_PHASES, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT_SUM_OVER_ALL_PHASES.unit == "A"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_CURRENT_SUM_OVER_ALL_PHASES.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_CURRENT_SUM_OVER_ALL_PHASES.value == 8

        # ESO_LT_FREQUENCY (1-0:14.7.0)
        assert isinstance(telegram.ESO_LT_FREQUENCY, CosemObject)
        assert telegram.ESO_LT_FREQUENCY.unit == "Hz"
        assert isinstance(telegram.ESO_LT_FREQUENCY.value, Decimal)
        assert telegram.ESO_LT_FREQUENCY.value == Decimal("49")

        # ESO_LT_INSTANTANEOUS_ACTIVE_POWER (1-0:15.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_ACTIVE_POWER, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_ACTIVE_POWER.unit == "kW"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_ACTIVE_POWER.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_ACTIVE_POWER.value == Decimal("1.915")

        # ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER (1-0:9.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER.value == Decimal("1.270")

        # ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L1 (1-0:29.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L1, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L1.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L1.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L1.value == Decimal("0")

        # ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L2 (1-0:49.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L2, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L2.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L2.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L2.value == Decimal("0")

        # ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L3 (1-0:69.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L3, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L3.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L3.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_IMPORT_POWER_L3.value == Decimal("1.270")

        # ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER (1-0:10.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER.value == Decimal("0.683")

        # ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L1 (1-0:30.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L1, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L1.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L1.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L1.value == Decimal("0.294")

        # ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L2 (1-0:50.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L2, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L2.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L2.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L2.value == Decimal("0.388")

        # ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L3 (1-0:70.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L3, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L3.unit == "kVA"
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L3.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_APPARENT_EXPORT_POWER_L3.value == Decimal("0")

        # ESO_LT_AVERAGE_IMPORT_POWER (1-0:1.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_IMPORT_POWER, CosemObject)
        assert telegram.ESO_LT_AVERAGE_IMPORT_POWER.unit == "kW"
        assert isinstance(telegram.ESO_LT_AVERAGE_IMPORT_POWER.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_IMPORT_POWER.value == Decimal("0.331")

        # ESO_LT_AVERAGE_NET_POWER (1-0:16.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_NET_POWER, CosemObject)
        assert telegram.ESO_LT_AVERAGE_NET_POWER.unit == "kW"
        assert isinstance(telegram.ESO_LT_AVERAGE_NET_POWER.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_NET_POWER.value == Decimal("1.068")

        # ESO_LT_AVERAGE_TOTAL_POWER (1-0:15.24.0)
        assert isinstance(telegram.ESO_LT_AVERAGE_TOTAL_POWER, CosemObject)
        assert telegram.ESO_LT_AVERAGE_TOTAL_POWER.unit == "kW"
        assert isinstance(telegram.ESO_LT_AVERAGE_TOTAL_POWER.value, Decimal)
        assert telegram.ESO_LT_AVERAGE_TOTAL_POWER.value == Decimal("1.075")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL (1-0:13.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_TOTAL.value == Decimal("0.945")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1 (1-0:33.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L1.value == Decimal("-0.926")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_L2 (1-0:53.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L2, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L2.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L2.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L2.value == Decimal("-0.984")

        # ESO_LT_INSTANTANEOUS_POWER_FACTOR_L3 (1-0:73.7.0)
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L3, CosemObject)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L3.unit is None
        assert isinstance(telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L3.value, Decimal)
        assert telegram.ESO_LT_INSTANTANEOUS_POWER_FACTOR_L3.value == Decimal("0.991")

        # ESO_LT_MINIMUM_POWER_FACTOR (1-0:13.3.0)
        assert isinstance(telegram.ESO_LT_MINIMUM_POWER_FACTOR, CosemObject)
        assert telegram.ESO_LT_MINIMUM_POWER_FACTOR.unit is None
        assert isinstance(telegram.ESO_LT_MINIMUM_POWER_FACTOR.value, Decimal)
        assert telegram.ESO_LT_MINIMUM_POWER_FACTOR.value == Decimal("0")

        # ESO_LT_MEASUREMENT_PERIOD_3_FOR_INSTANTANEOUS_VALUES (1-0:0.8.2)
        assert isinstance(telegram.ESO_LT_MEASUREMENT_PERIOD_3_FOR_INSTANTANEOUS_VALUES, CosemObject)
        assert telegram.ESO_LT_MEASUREMENT_PERIOD_3_FOR_INSTANTANEOUS_VALUES.unit == "s"
        assert isinstance(telegram.ESO_LT_MEASUREMENT_PERIOD_3_FOR_INSTANTANEOUS_VALUES.value, int)
        assert telegram.ESO_LT_MEASUREMENT_PERIOD_3_FOR_INSTANTANEOUS_VALUES.value == 900

        # ESO_LT_DEMAND_REGISTER_1_ACTIVE_ENERGY_IMPORT (1-0:1.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_1_ACTIVE_ENERGY_IMPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_1_ACTIVE_ENERGY_IMPORT.unit == "kW"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_1_ACTIVE_ENERGY_IMPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_1_ACTIVE_ENERGY_IMPORT.value == Decimal("0.337")

        # ESO_LT_DEMAND_REGISTER_2_ACTIVE_ENERGY_EXPORT (1-0:2.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_2_ACTIVE_ENERGY_EXPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_2_ACTIVE_ENERGY_EXPORT.unit == "kW"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_2_ACTIVE_ENERGY_EXPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_2_ACTIVE_ENERGY_EXPORT.value == Decimal("0.794")

        # ESO_LT_DEMAND_REGISTER_3_REACTIVE_ENERGY_IMPORT (1-0:3.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_3_REACTIVE_ENERGY_IMPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_3_REACTIVE_ENERGY_IMPORT.unit == "kvar"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_3_REACTIVE_ENERGY_IMPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_3_REACTIVE_ENERGY_IMPORT.value == Decimal("0.439")

        # ESO_LT_DEMAND_REGISTER_4_REACTIVE_ENERGY_EXPORT (1-0:4.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_4_REACTIVE_ENERGY_EXPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_4_REACTIVE_ENERGY_EXPORT.unit == "kvar"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_4_REACTIVE_ENERGY_EXPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_4_REACTIVE_ENERGY_EXPORT.value == Decimal("0.012")

        # ESO_LT_DEMAND_REGISTER_5_APPARENT_ENERGY_IMPORT (1-0:9.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_5_APPARENT_ENERGY_IMPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_5_APPARENT_ENERGY_IMPORT.unit == "kVA"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_5_APPARENT_ENERGY_IMPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_5_APPARENT_ENERGY_IMPORT.value == Decimal("0.352")

        # ESO_LT_DEMAND_REGISTER_6_APPARENT_ENERGY_EXPORT (1-0:10.4.0)
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_6_APPARENT_ENERGY_EXPORT, CosemObject)
        assert telegram.ESO_LT_DEMAND_REGISTER_6_APPARENT_ENERGY_EXPORT.unit == "kVA"
        assert isinstance(telegram.ESO_LT_DEMAND_REGISTER_6_APPARENT_ENERGY_EXPORT.value, Decimal)
        assert telegram.ESO_LT_DEMAND_REGISTER_6_APPARENT_ENERGY_EXPORT.value == Decimal("0.948")

        # SHORT_POWER_FAILURE_COUNT (0-0:96.7.21)
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT, CosemObject)
        assert telegram.SHORT_POWER_FAILURE_COUNT.unit is None
        assert isinstance(telegram.SHORT_POWER_FAILURE_COUNT.value, int)
        assert telegram.SHORT_POWER_FAILURE_COUNT.value == 285

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L1 (1-0:32.33.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L1, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L1.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L1.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L1.value == 736

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L2 (1-0:52.33.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L2, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L2.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L2.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L2.value == 734

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L3 (1-0:72.33.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L3, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L3.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L3.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SAG_L3.value == 736

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L1 (1-0:32.34.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L1, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L1.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L1.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L1.value == 0

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L2 (1-0:52.34.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L2, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L2.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L2.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L2.value == 0

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L3 (1-0:72.34.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L3, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L3.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L3.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SAG_L3.value == 0

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L1 (1-0:32.37.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L1, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L1.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L1.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L1.value == 284

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L2 (1-0:52.37.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L2, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L2.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L2.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L2.value == 347

        # ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L3 (1-0:72.37.0)
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L3, CosemObject)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L3.unit == "s"
        assert isinstance(telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L3.value, int)
        assert telegram.ESO_LT_DURATION_OF_LAST_VOLTAGE_SWELL_L3.value == 327

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L1 (1-0:32.38.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L1, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L1.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L1.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L1.value == 256

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L2 (1-0:52.38.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L2, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L2.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L2.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L2.value == 256

        # ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L3 (1-0:72.38.0)
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L3, CosemObject)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L3.unit == "V"
        assert isinstance(telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L3.value, int)
        assert telegram.ESO_LT_MAGNITUDE_OF_LAST_VOLTAGE_SWELL_L3.value == 256

        # ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER (1-0:0.2.0)
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER, CosemObject)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER.unit is None
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER.value, str)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER.value == "02.21"

        # ESO_LT_ACTIVE_FIRMWARE_SIGNATURE (1-0:0.2.8)
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE, CosemObject)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE.unit is None
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE.value, str)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE.value == "1EA43311"

        # ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER_1 (1-1:0.2.0)
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER_1, CosemObject)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER_1.unit is None
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER_1.value, str)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_IDENTIFIER_1.value == "03.02"

        # ESO_LT_ACTIVE_FIRMWARE_SIGNATURE_1 (1-1:0.2.8)
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE_1, CosemObject)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE_1.unit is None
        assert isinstance(telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE_1.value, str)
        assert telegram.ESO_LT_ACTIVE_FIRMWARE_SIGNATURE_1.value == "24408DB2"

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(telegram.TEXT_MESSAGE, CosemObject)
        assert telegram.TEXT_MESSAGE.unit is None
        assert isinstance(telegram.TEXT_MESSAGE.value, str)
        assert telegram.TEXT_MESSAGE.value == "73657450315F6D61785F337068"

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L1_COUNT.value == 45

        # VOLTAGE_SAG_L2_COUNT (1-0:52.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L2_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L2_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L2_COUNT.value == 49

        # VOLTAGE_SAG_L3_COUNT (1-0:72.32.0)
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT, CosemObject)
        assert telegram.VOLTAGE_SAG_L3_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SAG_L3_COUNT.value, int)
        assert telegram.VOLTAGE_SAG_L3_COUNT.value == 46

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L1_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L1_COUNT.value == 75

        # VOLTAGE_SWELL_L2_COUNT (1-0:52.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L2_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L2_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L2_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L2_COUNT.value == 141

        # VOLTAGE_SWELL_L3_COUNT (1-0:72.36.0)
        assert isinstance(telegram.VOLTAGE_SWELL_L3_COUNT, CosemObject)
        assert telegram.VOLTAGE_SWELL_L3_COUNT.unit is None
        assert isinstance(telegram.VOLTAGE_SWELL_L3_COUNT.value, int)
        assert telegram.VOLTAGE_SWELL_L3_COUNT.value == 78

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER, CosemObject)
        assert telegram.EQUIPMENT_IDENTIFIER.unit is None
        assert isinstance(telegram.EQUIPMENT_IDENTIFIER.value, str)
        assert telegram.EQUIPMENT_IDENTIFIER.value == "53414731303030303030303030303031"

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(
            TELEGRAM_V5_ESO_setP1_max_3ph
        )

    def test_checksum_invalid(self):
        corrupted = TELEGRAM_V5_ESO_setP1_max_3ph.replace(
            "1-0:1.8.1(007926.000*kWh)\r\n",
            ""
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted)

    def test_checksum_missing(self):
        corrupted = TELEGRAM_V5_ESO_setP1_max_3ph.replace(
            "!979F\r\n",
            ""
        )

        with self.assertRaises(ParseError):
            TelegramParser.validate_checksum(corrupted)
