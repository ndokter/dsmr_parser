import unittest

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.objects import CosemObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V5


class TelegramParserV5Test(unittest.TestCase):
    """ Test parsing of a DSMR v5.x telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V5)
        result = parser.parse(TELEGRAM_V5)

        # P1_MESSAGE_HEADER (1-3:0.2.8)
        assert isinstance(result[obis.P1_MESSAGE_HEADER], CosemObject)
        assert result[obis.P1_MESSAGE_HEADER].unit is None
        assert isinstance(result[obis.P1_MESSAGE_HEADER].value, str)
        assert result[obis.P1_MESSAGE_HEADER].value == '50'
