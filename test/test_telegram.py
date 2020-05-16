import unittest
import datetime
import pytz

from dsmr_parser import telegram_specifications
from dsmr_parser import obis_name_mapping
from dsmr_parser.objects import CosemObject
from dsmr_parser.objects import MBusObject
from dsmr_parser.objects import Telegram
from dsmr_parser.objects import ProfileGenericObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V4_2
from decimal import Decimal


class TelegramTest(unittest.TestCase):
    """ Test instantiation of Telegram object """

    def __init__(self, *args, **kwargs):
        self.item_names_tested = []
        super(TelegramTest, self).__init__(*args, **kwargs)

    def verify_telegram_item(self, telegram, testitem_name, object_type, unit_val, value_type, value_val):
        testitem = eval("telegram.{}".format(testitem_name))
        assert isinstance(testitem, object_type)
        assert testitem.unit == unit_val
        assert isinstance(testitem.value, value_type)
        assert testitem.value == value_val
        self.item_names_tested.append(testitem_name)

    def test_instantiate(self):
        parser = TelegramParser(telegram_specifications.V4)
        telegram = Telegram(TELEGRAM_V4_2, parser, telegram_specifications.V4)

        # P1_MESSAGE_HEADER (1-3:0.2.8)
        self.verify_telegram_item(telegram,
                                  'P1_MESSAGE_HEADER',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=str,
                                  value_val='42')

        # P1_MESSAGE_TIMESTAMP (0-0:1.0.0)
        self.verify_telegram_item(telegram,
                                  'P1_MESSAGE_TIMESTAMP',
                                  CosemObject,
                                  unit_val=None,
                                  value_type=datetime.datetime,
                                  value_val=datetime.datetime(2016, 11, 13, 19, 57, 57, tzinfo=pytz.UTC))

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        self.verify_telegram_item(telegram,
                                  'ELECTRICITY_USED_TARIFF_1',
                                  object_type=CosemObject,
                                  unit_val='kWh',
                                  value_type=Decimal,
                                  value_val=Decimal('1581.123'))

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        self.verify_telegram_item(telegram,
                                  'ELECTRICITY_USED_TARIFF_2',
                                  object_type=CosemObject,
                                  unit_val='kWh',
                                  value_type=Decimal,
                                  value_val=Decimal('1435.706'))

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        self.verify_telegram_item(telegram,
                                  'ELECTRICITY_DELIVERED_TARIFF_1',
                                  object_type=CosemObject,
                                  unit_val='kWh',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        self.verify_telegram_item(telegram,
                                  'ELECTRICITY_DELIVERED_TARIFF_2',
                                  object_type=CosemObject,
                                  unit_val='kWh',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        self.verify_telegram_item(telegram,
                                  'ELECTRICITY_ACTIVE_TARIFF',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=str,
                                  value_val='0002')

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        self.verify_telegram_item(telegram,
                                  'EQUIPMENT_IDENTIFIER',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=str,
                                  value_val='3960221976967177082151037881335713')

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        self.verify_telegram_item(telegram,
                                  'CURRENT_ELECTRICITY_USAGE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('2.027'))

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        self.verify_telegram_item(telegram,
                                  'CURRENT_ELECTRICITY_DELIVERY',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # SHORT_POWER_FAILURE_COUNT (1-0:96.7.21)
        self.verify_telegram_item(telegram,
                                  'SHORT_POWER_FAILURE_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=15)

        # LONG_POWER_FAILURE_COUNT (96.7.9)
        self.verify_telegram_item(telegram,
                                  'LONG_POWER_FAILURE_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=7)

        # VOLTAGE_SAG_L1_COUNT (1-0:32.32.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SAG_L1_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # VOLTAGE_SAG_L2_COUNT (1-0:52.32.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SAG_L2_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # VOLTAGE_SAG_L3_COUNT (1-0:72.32.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SAG_L3_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # VOLTAGE_SWELL_L1_COUNT (1-0:32.36.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SWELL_L1_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # VOLTAGE_SWELL_L2_COUNT (1-0:52.36.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SWELL_L2_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # VOLTAGE_SWELL_L3_COUNT (1-0:72.36.0)
        self.verify_telegram_item(telegram,
                                  'VOLTAGE_SWELL_L3_COUNT',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=0)

        # TEXT_MESSAGE_CODE (0-0:96.13.1)
        self.verify_telegram_item(telegram,
                                  'TEXT_MESSAGE_CODE',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=type(None),
                                  value_val=None)

        # TEXT_MESSAGE (0-0:96.13.0)
        self.verify_telegram_item(telegram,
                                  'TEXT_MESSAGE',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=type(None),
                                  value_val=None)

        # INSTANTANEOUS_CURRENT_L1 (1-0:31.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_CURRENT_L1',
                                  object_type=CosemObject,
                                  unit_val='A',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # INSTANTANEOUS_CURRENT_L2 (1-0:51.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_CURRENT_L2',
                                  object_type=CosemObject,
                                  unit_val='A',
                                  value_type=Decimal,
                                  value_val=Decimal('6'))

        # INSTANTANEOUS_CURRENT_L3 (1-0:71.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_CURRENT_L3',
                                  object_type=CosemObject,
                                  unit_val='A',
                                  value_type=Decimal,
                                  value_val=Decimal('2'))

        # DEVICE_TYPE (0-x:24.1.0)
        self.verify_telegram_item(telegram,
                                  'DEVICE_TYPE',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=int,
                                  value_val=3)

        # INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE (1-0:21.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0.170'))

        # INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE (1-0:41.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('1.247'))

        # INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE (1-0:61.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0.209'))

        # INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE (1-0:22.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE (1-0:42.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE (1-0:62.7.0)
        self.verify_telegram_item(telegram,
                                  'INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE',
                                  object_type=CosemObject,
                                  unit_val='kW',
                                  value_type=Decimal,
                                  value_val=Decimal('0'))

        # EQUIPMENT_IDENTIFIER_GAS (0-x:96.1.0)
        self.verify_telegram_item(telegram,
                                  'EQUIPMENT_IDENTIFIER_GAS',
                                  object_type=CosemObject,
                                  unit_val=None,
                                  value_type=str,
                                  value_val='4819243993373755377509728609491464')

        # HOURLY_GAS_METER_READING (0-1:24.2.1)
        self.verify_telegram_item(telegram,
                                  'HOURLY_GAS_METER_READING',
                                  object_type=MBusObject,
                                  unit_val='m3',
                                  value_type=Decimal,
                                  value_val=Decimal('981.443'))

        # POWER_EVENT_FAILURE_LOG (1-0:99.97.0)
        testitem_name = 'POWER_EVENT_FAILURE_LOG'
        object_type = ProfileGenericObject
        testitem = eval("telegram.{}".format(testitem_name))
        assert isinstance(testitem, object_type)
        assert testitem.buffer_length == 3
        assert testitem.buffer_type == '0-0:96.7.19'
        buffer = testitem.buffer
        assert isinstance(testitem.buffer, list)
        assert len(buffer) == 3
        assert all([isinstance(item, MBusObject) for item in buffer])
        date0 = datetime.datetime(2000, 1, 4, 17, 3, 20, tzinfo=datetime.timezone.utc)
        date1 = datetime.datetime(1999, 12, 31, 23, 0, 1, tzinfo=datetime.timezone.utc)
        date2 = datetime.datetime(2000, 1, 1, 23, 0, 3, tzinfo=datetime.timezone.utc)
        assert buffer[0].datetime == date0
        assert buffer[1].datetime == date1
        assert buffer[2].datetime == date2
        assert buffer[0].value == 237126
        assert buffer[1].value == 2147583646
        assert buffer[2].value == 2317482647
        assert all([isinstance(item.value, int) for item in buffer])
        assert all([isinstance(item.unit, str) for item in buffer])
        assert all([(item.unit == 's') for item in buffer])
        self.item_names_tested.append(testitem_name)

        # check if all items in telegram V4 specification are covered
        V4_name_list = [obis_name_mapping.EN[signature] for signature, parser in
                        telegram_specifications.V4['objects'].items()]
        V4_name_set = set(V4_name_list)
        item_names_tested_set = set(self.item_names_tested)

        assert item_names_tested_set == V4_name_set
