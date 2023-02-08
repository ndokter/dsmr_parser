import unittest
import datetime
import pytz

from dsmr_parser import telegram_specifications
from dsmr_parser import obis_name_mapping
from dsmr_parser import obis_references as obis
from dsmr_parser.objects import CosemObject, MbusDevice
from dsmr_parser.objects import MBusObject
from dsmr_parser.objects import ProfileGenericObject
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V4_2, TELEGRAM_V5_TWO_MBUS
from decimal import Decimal


class DeviceObjectTest(unittest.TestCase):

    def test_tmp(self):
        parser = TelegramParser(telegram_specifications.V5)
        telegram = parser.parse(TELEGRAM_V5_TWO_MBUS)
        # print('val: ', telegram.HOURLY_GAS_METER_READING)

        device = MbusDevice()
