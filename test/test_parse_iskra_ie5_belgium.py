import datetime
import unittest

from decimal import Decimal

from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError
from dsmr_parser.objects import CosemObject, MBusObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_ISKRA_IE5_BELGIUM


class TelegramParserIskraIE5BelgiumTest(unittest.TestCase):
    """
    Test parsing of a Belgian Iskra IE.5 telegram (issue #200).

    This meter sends 1-0:1.6.0 as (value)(timestamp) instead of
    (timestamp)(value), and without a DST flag on the timestamp.
    """

    def setUp(self):
        parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
        self.result = parser.parse(TELEGRAM_ISKRA_IE5_BELGIUM, throw_ex=True)

    def test_maximum_demand_month(self):
        # 1-0:1.6.0(006.4*kW)(261023051500)
        max_demand = self.result.BELGIUM_MAXIMUM_DEMAND_MONTH
        assert isinstance(max_demand, MBusObject)
        assert max_demand.value == Decimal('6.4')
        assert max_demand.unit == 'kW'
        # 05:15 local time without DST flag; Europe/Amsterdam is UTC+2 then.
        assert max_demand.datetime == datetime.datetime(
            2026, 10, 23, 3, 15, 0, tzinfo=datetime.timezone.utc
        )

    def test_other_values(self):
        r = self.result

        assert r.BELGIUM_VERSION_INFORMATION.value == '3231313130'
        assert r.BELGIUM_EQUIPMENT_IDENTIFIER.value == '3938363835333435'
        assert r.P1_MESSAGE_TIMESTAMP.value == datetime.datetime(
            2026, 10, 23, 11, 37, 55, tzinfo=datetime.timezone.utc
        )

        assert isinstance(r.ELECTRICITY_USED_TARIFF_1, CosemObject)
        assert r.ELECTRICITY_USED_TARIFF_1.value == Decimal('20.381')
        assert r.ELECTRICITY_USED_TARIFF_1.unit == 'kWh'
        assert r.ELECTRICITY_USED_TARIFF_2.value == Decimal('89.794')

        assert r.ELECTRICITY_ACTIVE_TARIFF.value == '0002'
        assert r.BELGIUM_CURRENT_AVERAGE_DEMAND.value == Decimal('0.1')
        assert r.CURRENT_ELECTRICITY_USAGE.value == Decimal('0.2')

        assert r.INSTANTANEOUS_VOLTAGE_L1.value == Decimal('129.5')
        assert r.INSTANTANEOUS_VOLTAGE_L1.unit == 'V'
        assert r.INSTANTANEOUS_CURRENT_L1.value == Decimal('1.32')
        assert r.INSTANTANEOUS_CURRENT_L1.unit == 'A'

        assert r.ACTUAL_TRESHOLD_ELECTRICITY.value == Decimal('999.9')
        assert r.ACTUAL_TRESHOLD_ELECTRICITY.unit == 'kVA'
        assert r.FUSE_THRESHOLD_L1.value == Decimal('999')
        assert r.TEXT_MESSAGE.value is None

    def test_checksum_valid(self):
        # No exception is raised.
        TelegramParser.validate_checksum(TELEGRAM_ISKRA_IE5_BELGIUM)

    def test_checksum_invalid(self):
        corrupted_telegram = TELEGRAM_ISKRA_IE5_BELGIUM.replace(
            '1-0:1.8.1(000020.381*kWh)\r\n',
            ''
        )

        with self.assertRaises(InvalidChecksumError):
            TelegramParser.validate_checksum(corrupted_telegram)
