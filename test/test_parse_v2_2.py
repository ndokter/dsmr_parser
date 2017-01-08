import unittest

from test.example_telegrams import TELEGRAM_V2_2
from dsmr_parser.parsers import TelegramParserV2_2
from dsmr_parser import telegram_specifications
from dsmr_parser import obis_references as obis


class TelegramParserV2_2Test(unittest.TestCase):
    """ Test parsing of a DSMR v2.2 telegram. """

    def test_parse(self):
        parser = TelegramParserV2_2(telegram_specifications.V2_2)
        result = parser.parse(TELEGRAM_V2_2)

        assert float(result[obis.CURRENT_ELECTRICITY_USAGE].value) == 1.01
        assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'

        assert float(result[obis.GAS_METER_READING].value) == 1.001
        assert result[obis.GAS_METER_READING].unit == 'm3'
