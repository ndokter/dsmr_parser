import unittest

from dsmr_parser.parsers import match_telegram_specification
from dsmr_parser import telegram_specifications
from test import example_telegrams


class MatchTelegramSpecificationTest(unittest.TestCase):


    def test_v2_2(self):
        assert match_telegram_specification(example_telegrams.TELEGRAM_V2_2) \
           == telegram_specifications.V2_2

    def test_v3(self):
        assert match_telegram_specification(example_telegrams.TELEGRAM_V3) \
           == telegram_specifications.V3

    def test_v4_2(self):
        assert match_telegram_specification(example_telegrams.TELEGRAM_V4_2) \
           == telegram_specifications.V4

    def test_v5(self):
        assert match_telegram_specification(example_telegrams.TELEGRAM_V5) \
           == telegram_specifications.V5
