import unittest

from decimal import Decimal

from dsmr_parser.objects import CosemObject, MBusObject
from dsmr_parser.parsers import TelegramParser
from dsmr_parser import telegram_specifications
from dsmr_parser import obis_references as obis
from test.example_telegrams import TELEGRAM_V3


class TelegramParserV3Test(unittest.TestCase):
    """ Test parsing of a DSMR v3 telegram. """

    def test_parse(self):
        parser = TelegramParser(telegram_specifications.V3)
        result = parser.parse(TELEGRAM_V3)

        # ELECTRICITY_USED_TARIFF_1 (1-0:1.8.1)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_1].value == Decimal('12345.678')

        # ELECTRICITY_USED_TARIFF_2 (1-0:1.8.2)
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_USED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_USED_TARIFF_2].value == Decimal('12345.678')

        # ELECTRICITY_DELIVERED_TARIFF_1 (1-0:2.8.1)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_1].value == Decimal('12345.678')

        # ELECTRICITY_DELIVERED_TARIFF_2 (1-0:2.8.2)
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2], CosemObject)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].unit == 'kWh'
        assert isinstance(result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value, Decimal)
        assert result[obis.ELECTRICITY_DELIVERED_TARIFF_2].value == Decimal('12345.678')

        # ELECTRICITY_ACTIVE_TARIFF (0-0:96.14.0)
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF], CosemObject)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].unit is None
        assert isinstance(result[obis.ELECTRICITY_ACTIVE_TARIFF].value, str)
        assert result[obis.ELECTRICITY_ACTIVE_TARIFF].value == '0002'

        # EQUIPMENT_IDENTIFIER (0-0:96.1.1)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER].value == '4B384547303034303436333935353037'

        # CURRENT_ELECTRICITY_USAGE (1-0:1.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_USAGE].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_USAGE].value == Decimal('1.19')

        # CURRENT_ELECTRICITY_DELIVERY (1-0:2.7.0)
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY], CosemObject)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].unit == 'kW'
        assert isinstance(result[obis.CURRENT_ELECTRICITY_DELIVERY].value, Decimal)
        assert result[obis.CURRENT_ELECTRICITY_DELIVERY].value == Decimal('0')

        # TEXT_MESSAGE_CODE (0-0:96.13.1)
        assert isinstance(result[obis.TEXT_MESSAGE_CODE], CosemObject)
        assert result[obis.TEXT_MESSAGE_CODE].unit is None
        assert isinstance(result[obis.TEXT_MESSAGE_CODE].value, int)
        assert result[obis.TEXT_MESSAGE_CODE].value == 303132333435363738

        # TEXT_MESSAGE (0-0:96.13.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.TEXT_MESSAGE].unit is None
        assert isinstance(result[obis.TEXT_MESSAGE].value, str)
        assert result[obis.TEXT_MESSAGE].value == \
            '303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F' \
            '303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F' \
            '303132333435363738393A3B3C3D3E3F'

        # DEVICE_TYPE (0-x:24.1.0)
        assert isinstance(result[obis.TEXT_MESSAGE], CosemObject)
        assert result[obis.DEVICE_TYPE].unit is None
        assert isinstance(result[obis.DEVICE_TYPE].value, str)
        assert result[obis.DEVICE_TYPE].value == '03'

        # EQUIPMENT_IDENTIFIER_GAS (0-x:96.1.0)
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS], CosemObject)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].unit is None
        assert isinstance(result[obis.EQUIPMENT_IDENTIFIER_GAS].value, str)
        assert result[obis.EQUIPMENT_IDENTIFIER_GAS].value == '3232323241424344313233343536373839'

        # GAS_METER_READING (0-1:24.3.0)
        assert isinstance(result[obis.GAS_METER_READING], MBusObject)
        assert result[obis.GAS_METER_READING].unit == 'm3'
        assert isinstance(result[obis.GAS_METER_READING].value, Decimal)
        assert result[obis.GAS_METER_READING].value == Decimal('1.001')
