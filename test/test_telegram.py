from decimal import Decimal

import datetime
import unittest

import pytz

from dsmr_parser import obis_references as obis
from dsmr_parser import telegram_specifications
from dsmr_parser.exceptions import InvalidChecksumError, ParseError
from dsmr_parser.objects import CosemObject, MBusObject, Telegram
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V4_2

class TelegramTest(unittest.TestCase):
    """ Test instantiation of Telegram object """

    def test_instantiate(self):
        parser = TelegramParser(telegram_specifications.V4)
        #result = parser.parse(TELEGRAM_V4_2)
        telegram = Telegram(TELEGRAM_V4_2, parser, telegram_specifications.V4)




        # P1_MESSAGE_HEADER (1-3:0.2.8)
        #assert isinstance(result[obis.P1_MESSAGE_HEADER], CosemObject)
        #assert result[obis.P1_MESSAGE_HEADER].unit is None
        #assert isinstance(result[obis.P1_MESSAGE_HEADER].value, str)
        #assert result[obis.P1_MESSAGE_HEADER].value == '50'
