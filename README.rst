DSMR Parser
===========

.. image:: https://img.shields.io/pypi/v/dsmr-parser.svg
    :target: https://pypi.python.org/pypi/dsmr-parser

.. image:: https://travis-ci.org/ndokter/dsmr_parser.svg?branch=master
    :target: https://travis-ci.org/ndokter/dsmr_parser

A library for parsing Dutch Smart Meter Requirements (DSMR) telegram data. It
also includes client implementation to directly read and parse smart meter data.


Features
--------

DSMR Parser supports DSMR versions 2, 3, 4 and 5. It has been tested with Python 3.5, 3.6, 3.7, 3.8 and 3.9.


Client module usage
-------------------

**Serial client**

Read the serial port and work with the parsed telegrams. It should be run in a separate
process because the code is blocking (not asynchronous):

.. code-block:: python

     from dsmr_parser import telegram_specifications
     from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
    
     serial_reader = SerialReader(
         device='/dev/ttyUSB0',
         serial_settings=SERIAL_SETTINGS_V4,
         telegram_specification=telegram_specifications.V4
     )
    
     for telegram in serial_reader.read():
         print(telegram)  # see 'Telegram object' docs below

**AsyncIO client**

To be documented.


Parsing module usage
--------------------
The parsing module accepts complete unaltered telegram strings and parses these
into a dictionary.

.. code-block:: python

     from dsmr_parser import telegram_specifications
     from dsmr_parser.parsers import TelegramParser

     # String is formatted in separate lines for readability.
     telegram_str = (
         '/ISk5\\2MT382-1000\r\n'
         '\r\n'
         '0-0:96.1.1(4B384547303034303436333935353037)\r\n'
         '1-0:1.8.1(12345.678*kWh)\r\n'
         '1-0:1.8.2(12345.678*kWh)\r\n'
         '1-0:2.8.1(12345.678*kWh)\r\n'
         '1-0:2.8.2(12345.678*kWh)\r\n'
         '0-0:96.14.0(0002)\r\n'
         '1-0:1.7.0(001.19*kW)\r\n'
         '1-0:2.7.0(000.00*kW)\r\n'
         '0-0:17.0.0(016*A)\r\n'
         '0-0:96.3.10(1)\r\n'
         '0-0:96.13.1(303132333435363738)\r\n'
         '0-0:96.13.0(303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E'
         '3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F30313233'
         '3435363738393A3B3C3D3E3F)\r\n'
         '0-1:96.1.0(3232323241424344313233343536373839)\r\n'
         '0-1:24.1.0(03)\r\n'
         '0-1:24.3.0(090212160000)(00)(60)(1)(0-1:24.2.1)(m3)\r\n'
         '(00001.001)\r\n'
         '0-1:24.4.0(1)\r\n'
         '!\r\n'
     )

     parser = TelegramParser(telegram_specifications.V3)
    
     telegram = parser.parse(telegram_str)
     print(telegram)  # see 'Telegram object' docs below

Telegram dictionary
-------------------

A dictionary of which the key indicates the field type. These regex values
correspond to one of dsmr_parser.obis_reference constants.

The value is either a CosemObject or MBusObject. These have a 'value' and 'unit'
property. MBusObject's additionally have a 'datetime' property. The 'value' can
contain any python type (int, str, Decimal) depending on the field. The 'unit'
contains 'kW', 'A', 'kWh' or 'm3'.

.. code-block:: python

    # Contents of a parsed DSMR v3 telegram
    {'\\d-\\d:17\\.0\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39eb8>,
     '\\d-\\d:1\\.7\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10f916390>,
     '\\d-\\d:1\\.8\\.1.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39e10>,
     '\\d-\\d:1\\.8\\.2.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39ef0>,
     '\\d-\\d:24\\.1\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fbaef28>,
     '\\d-\\d:24\\.3\\.0.+?\\r\\n.+?\\r\\n': <dsmr_parser.objects.MBusObject object at 0x10f9163c8>,
     '\\d-\\d:24\\.4\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39f60>,
     '\\d-\\d:2\\.7\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39fd0>,
     '\\d-\\d:2\\.8\\.1.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fbaee10>,
     '\\d-\\d:2\\.8\\.2.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39e80>,
     '\\d-\\d:96\\.13\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39d30>,
     '\\d-\\d:96\\.13\\.1.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fbaeeb8>,
     '\\d-\\d:96\\.14\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fbaef98>,
     '\\d-\\d:96\\.1\\.0.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fbaef60>,
     '\\d-\\d:96\\.1\\.1.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39f98>,
     '\\d-\\d:96\\.3\\.10.+?\\r\\n': <dsmr_parser.objects.CosemObject object at 0x10fc39dd8>}

Example to get some of the values:

.. code-block:: python

    from dsmr_parser import obis_references

     # The telegram message timestamp.
     message_datetime = telegram[obis_references.P1_MESSAGE_TIMESTAMP]

     # Using the active tariff to determine the electricity being used and
     # delivered for the right tariff.
     active_tariff = telegram[obis_references.ELECTRICITY_ACTIVE_TARIFF]
     active_tariff = int(tariff.value)

     electricity_used_total = telegram[obis_references.ELECTRICITY_USED_TARIFF_ALL[active_tariff - 1]]
     electricity_delivered_total = telegram[obis_references.ELECTRICITY_DELIVERED_TARIFF_ALL[active_tariff - 1]]

     gas_reading = telegram[obis_references.HOURLY_GAS_METER_READING]

    # See dsmr_reader.obis_references for all readable telegram values.
    # Note that the avilable values differ per DSMR version.

Telegram as an Object
---------------------
An object version of the telegram is available as well.


.. code-block:: python

    # DSMR v4.2 p1 using dsmr_parser and telegram objects

    from dsmr_parser import telegram_specifications
    from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
    from dsmr_parser.objects import CosemObject, MBusObject, Telegram
    from dsmr_parser.parsers import TelegramParser
    import os

    serial_reader = SerialReader(
        device='/dev/ttyUSB0',
        serial_settings=SERIAL_SETTINGS_V5,
        telegram_specification=telegram_specifications.V4
    )

    # telegram = next(serial_reader.read_as_object())
    # print(telegram)

    for telegram in serial_reader.read_as_object():
        os.system('clear')
        print(telegram)

Example of output of print of the telegram object:

.. code-block:: console

    P1_MESSAGE_HEADER: 	 42 	[None]
    P1_MESSAGE_TIMESTAMP: 	 2016-11-13 19:57:57+00:00 	[None]
    EQUIPMENT_IDENTIFIER: 	 3960221976967177082151037881335713 	[None]
    ELECTRICITY_USED_TARIFF_1: 	 1581.123 	[kWh]
    ELECTRICITY_USED_TARIFF_2: 	 1435.706 	[kWh]
    ELECTRICITY_DELIVERED_TARIFF_1: 	 0.000 	[kWh]
    ELECTRICITY_DELIVERED_TARIFF_2: 	 0.000 	[kWh]
    ELECTRICITY_ACTIVE_TARIFF: 	 0002 	[None]
    CURRENT_ELECTRICITY_USAGE: 	 2.027 	[kW]
    CURRENT_ELECTRICITY_DELIVERY: 	 0.000 	[kW]
    LONG_POWER_FAILURE_COUNT: 	 7 	[None]
    VOLTAGE_SAG_L1_COUNT: 	 0 	[None]
    VOLTAGE_SAG_L2_COUNT: 	 0 	[None]
    VOLTAGE_SAG_L3_COUNT: 	 0 	[None]
    VOLTAGE_SWELL_L1_COUNT: 	 0 	[None]
    VOLTAGE_SWELL_L2_COUNT: 	 0 	[None]
    VOLTAGE_SWELL_L3_COUNT: 	 0 	[None]
    TEXT_MESSAGE_CODE: 	 None 	[None]
    TEXT_MESSAGE: 	 None 	[None]
    DEVICE_TYPE: 	 3 	[None]
    INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE: 	 0.170 	[kW]
    INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE: 	 1.247 	[kW]
    INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE: 	 0.209 	[kW]
    INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE: 	 0.000 	[kW]
    INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE: 	 0.000 	[kW]
    INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE: 	 0.000 	[kW]
    EQUIPMENT_IDENTIFIER_GAS: 	 4819243993373755377509728609491464 	[None]
    HOURLY_GAS_METER_READING: 	 981.443 	[m3]

Accessing the telegrams information as  attributes directly:

.. code-block:: python

    telegram
    Out[3]: <dsmr_parser.objects.Telegram at 0x7f5e995d9898>
    telegram.CURRENT_ELECTRICITY_USAGE
    Out[4]: <dsmr_parser.objects.CosemObject at 0x7f5e98ae5ac8>
    telegram.CURRENT_ELECTRICITY_USAGE.value
    Out[5]: Decimal('2.027')
    telegram.CURRENT_ELECTRICITY_USAGE.unit
    Out[6]: 'kW'

The telegram object has an iterator, can be used to find all the information elements in the current telegram:

.. code-block:: python

    [attr for attr, value in telegram]
    Out[11]:
    ['P1_MESSAGE_HEADER',
     'P1_MESSAGE_TIMESTAMP',
     'EQUIPMENT_IDENTIFIER',
     'ELECTRICITY_USED_TARIFF_1',
     'ELECTRICITY_USED_TARIFF_2',
     'ELECTRICITY_DELIVERED_TARIFF_1',
     'ELECTRICITY_DELIVERED_TARIFF_2',
     'ELECTRICITY_ACTIVE_TARIFF',
     'CURRENT_ELECTRICITY_USAGE',
     'CURRENT_ELECTRICITY_DELIVERY',
     'LONG_POWER_FAILURE_COUNT',
     'VOLTAGE_SAG_L1_COUNT',
     'VOLTAGE_SAG_L2_COUNT',
     'VOLTAGE_SAG_L3_COUNT',
     'VOLTAGE_SWELL_L1_COUNT',
     'VOLTAGE_SWELL_L2_COUNT',
     'VOLTAGE_SWELL_L3_COUNT',
     'TEXT_MESSAGE_CODE',
     'TEXT_MESSAGE',
     'DEVICE_TYPE',
     'INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE',
     'INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE',
     'INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE',
     'INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE',
     'INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE',
     'INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE',
     'EQUIPMENT_IDENTIFIER_GAS',
     'HOURLY_GAS_METER_READING']


Installation
------------

To install DSMR Parser:

.. code-block:: bash

    $ pip install dsmr-parser

Known issues
------------

If the serial settings SERIAL_SETTINGS_V2_2 or SERIAL_SETTINGS_V4 don't work.
Make sure to try and replace the parity settings to EVEN or NONE.
It's possible that alternative settings will be added in the future if these
settings don't work for the majority of meters.
