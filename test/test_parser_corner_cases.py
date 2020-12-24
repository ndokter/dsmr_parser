import unittest

from dsmr_parser import telegram_specifications

from dsmr_parser.objects import Telegram
from dsmr_parser.objects import ProfileGenericObject
from dsmr_parser.parsers import TelegramParser
from dsmr_parser.parsers import ProfileGenericParser
from dsmr_parser.profile_generic_specifications import BUFFER_TYPES
from dsmr_parser.profile_generic_specifications import PG_HEAD_PARSERS
from dsmr_parser.profile_generic_specifications import PG_UNIDENTIFIED_BUFFERTYPE_PARSERS
from test.example_telegrams import TELEGRAM_V5


class TestParserCornerCases(unittest.TestCase):
    """ Test instantiation of Telegram object """

    def test_power_event_log_empty_1(self):
        # POWER_EVENT_FAILURE_LOG (1-0:99.97.0)
        parser = TelegramParser(telegram_specifications.V5)
        telegram = Telegram(TELEGRAM_V5, parser, telegram_specifications.V5)

        object_type = ProfileGenericObject
        testitem = telegram.POWER_EVENT_FAILURE_LOG
        assert isinstance(testitem, object_type)
        assert testitem.buffer_length == 0
        assert testitem.buffer_type == '0-0:96.7.19'
        buffer = testitem.buffer
        assert isinstance(testitem.buffer, list)
        assert len(buffer) == 0

    def test_power_event_log_empty_2(self):
        pef_parser = ProfileGenericParser(BUFFER_TYPES, PG_HEAD_PARSERS, PG_UNIDENTIFIED_BUFFERTYPE_PARSERS)
        object_type = ProfileGenericObject

        # Power Event Log with 0 items and no object type
        pefl_line = r'1-0:99.97.0(0)()\r\n'
        testitem = pef_parser.parse(pefl_line)

        assert isinstance(testitem, object_type)
        assert testitem.buffer_length == 0
        assert testitem.buffer_type is None
        buffer = testitem.buffer
        assert isinstance(testitem.buffer, list)
        assert len(buffer) == 0
        assert testitem.values == [{'value': 0, 'unit': None}, {'value': None, 'unit': None}]
        json = testitem.to_json()
        assert json == '{"buffer_length": 0, "buffer_type": null, "buffer": []}'

    def test_power_event_log_null_values(self):
        pef_parser = ProfileGenericParser(BUFFER_TYPES, PG_HEAD_PARSERS, PG_UNIDENTIFIED_BUFFERTYPE_PARSERS)
        object_type = ProfileGenericObject

        # Power Event Log with 1 item and no object type and nno values for the item
        pefl_line = r'1-0:99.97.0(1)()()()\r\n'
        testitem = pef_parser.parse(pefl_line)

        assert isinstance(testitem, object_type)
        assert testitem.buffer_length == 1
        assert testitem.buffer_type is None
        buffer = testitem.buffer
        assert isinstance(testitem.buffer, list)
        assert len(buffer) == 1
        assert testitem.values == [{'value': 1, 'unit': None}, {'value': None, 'unit': None},
                                   {'value': None, 'unit': None}, {'value': None, 'unit': None}]
        json = testitem.to_json()
        assert json == \
               '{"buffer_length": 1, "buffer_type": null, "buffer": [{"datetime": null, "value": null, "unit": null}]}'

    def test_power_event_log_brackets_only(self):
        # POWER_EVENT_FAILURE_LOG (1-0:99.97.0)
        # Issue 57
        # Test of an ill formatted empty POWER_EVENT_FAILURE_LOG, observed on some smartmeters
        # The idea is that instead of failing, the parser converts it to an empty POWER_EVENT_FAILURE_LOG
        pef_parser = ProfileGenericParser(BUFFER_TYPES, PG_HEAD_PARSERS, PG_UNIDENTIFIED_BUFFERTYPE_PARSERS)
        object_type = ProfileGenericObject

        pefl_line = r'1-0:99.97.0()\r\n'
        testitem = pef_parser.parse(pefl_line)

        assert isinstance(testitem, object_type)
        assert testitem.buffer_length == 0
        assert testitem.buffer_type is None
        buffer = testitem.buffer
        assert isinstance(testitem.buffer, list)
        assert len(buffer) == 0
        assert testitem.values == [{'value': 0, 'unit': None}, {'value': None, 'unit': None}]
        json = testitem.to_json()
        assert json == '{"buffer_length": 0, "buffer_type": null, "buffer": []}'
