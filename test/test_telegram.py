import unittest

from dsmr_parser import telegram_specifications
from dsmr_parser.objects import CosemObject
from dsmr_parser.objects import Telegram
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V4_2


class TelegramTest(unittest.TestCase):
    """ Test instantiation of Telegram object """

    def test_instantiate(self):
        parser = TelegramParser(telegram_specifications.V4)
        telegram = Telegram(TELEGRAM_V4_2, parser, telegram_specifications.V4)

        # P1_MESSAGE_HEADER (1-3:0.2.8)
        testitem = telegram.P1_MESSAGE_HEADER
        assert isinstance(testitem, CosemObject)
        assert testitem.unit is None
        assert testitem.value == '42'
