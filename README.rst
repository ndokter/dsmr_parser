DSMR Parser
===========

.. image:: https://img.shields.io/pypi/v/dsmr-parser.svg
    :target: https://pypi.python.org/pypi/dsmr-parser

.. image:: https://img.shields.io/github/actions/workflow/status/ndokter/dsmr_parser/tests.yml?branch=master
    :target: https://github.com/ndokter/dsmr_parser/actions/workflows/tests.yml

A library for parsing Dutch Smart Meter Requirements (DSMR) telegram data. It
also includes client implementation to directly read and parse smart meter data.


Features
--------

DSMR Parser supports DSMR versions 2, 3, 4 and 5. See for the `currently supported/tested Python versions here <https://github.com/ndokter/dsmr_parser/blob/master/.github/workflows/tests.yml#L14>`_.

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

**Socket client**

Read a remote serial port (for example using ser2net) and work with the parsed telegrams.
It should be run in a separate process because the code is blocking (not asynchronous):

.. code-block:: python

     from dsmr_parser import telegram_specifications
     from dsmr_parser.clients import SocketReader
    
     socket_reader = SocketReader(
         host='127.0.0.1',
         port=2001,
         telegram_specification=telegram_specifications.V4
     )
    
     for telegram in socket_reader.read():
         print(telegram)  # see 'Telegram object' docs below

**AsyncIO client**

For a test run using a tcp server (lasting 20 seconds) use the following example:

.. code-block:: python

    import asyncio
    import logging
    from dsmr_parser import obis_references
    from dsmr_parser.clients.protocol import create_dsmr_reader, create_tcp_dsmr_reader

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    HOST = MY_HOST
    PORT = MY_PORT
    DSMR_VERSION = MY_DSMR_VERSION

    logger = logging.getLogger('tcpclient')
    logger.debug("Logger created")

    def printTelegram(telegram):
        logger.info(telegram)


    async def main():
        try:
            logger.debug("Getting loop")
            loop = asyncio.get_event_loop()
            logger.debug("Creating reader")
            await 	create_tcp_dsmr_reader(
                                HOST,
                                PORT,
                                DSMR_VERSION,
                                printTelegram,
                                loop
                                )
            logger.debug("Reader created going to sleep now")					
            await asyncio.sleep(20)
            logger.info('Finished run')					
        except Exception as e:
            logger.error("Unexpected error: "+ e)

    asyncio.run(main())

Note the creation of a callback function to call when a telegram is received. In this case `printTelegram`. Normally the used loop is the one running.

Currently the asyncio implementation does not support returning telegram objects directly as a `read_as_object()` for async tcp is currently not implemented.
Moreover, the telegram passed to `telegram_callback(telegram)` is already parsed. Therefore we can't feed it into the telegram constructor directly as that expects unparsed telegrams

However, if we construct a mock TelegramParser that just returns the already parsed object we can work around this. An example is below:

.. code-block:: python

    import asyncio
    import logging
    from dsmr_parser import telegram_specifications
    from dsmr_parser.clients.protocol import create_tcp_dsmr_reader

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    HOST = MY_HOST
    PORT = MY_PORT
    DSMR_VERSION = MY_DSMR_VERSION

    logger = logging.getLogger('tcpclient')
    logger.debug("Logger created")

    class mockTelegramParser(object):

        def parse(self, telegram):
            return telegram

    telegram_parser = mockTelegramParser()

    def printTelegram(telegram):
        try:
            logger.info(Telegram(telegram, telegram_parser, telegram_specifications.V4))
        except InvalidChecksumError as e:
            logger.warning(str(e))
        except ParseError as e:
            logger.error('Failed to parse telegram: %s', e)

    async def main():
        try:
            logger.debug("Getting loop")
            loop = asyncio.get_event_loop()
            logger.debug("Creating reader")
            await create_tcp_dsmr_reader(
                HOST,
                PORT,
                DSMR_VERSION,
                printTelegram,
                loop
            )
            logger.debug("Reader created going to sleep now")					
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            logger.error("Unexpected error: "+ e)
            raise

    if __name__ == '__main__':
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info('Closing down...')					
        except Exception as e:
            logger.error("Unexpected error: "+ e)

Parsing module usage
--------------------
The parsing module accepts complete unaltered telegram strings and parses these
into a Telegram object.

Tip: getting full telegrams from a bytestream can be made easier by using the TelegramBuffer helper class.

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

    # see 'Telegram object' docs below
    telegram = parser.parse(telegram_str)

Telegram object
---------------------

A Telegram has attributes for all the parsed values according to the given telegram specification. Each value is a DsmrObject which have a 'value' and 'unit' property. MBusObject's, which are DsmrObject's as well additionally have a 'datetime' property. The 'value' can contain any python type (int, str, Decimal) depending on the field. The 'unit' contains 'kW', 'A', 'kWh' or 'm3'.

Note: Telegram extends dictionary, which done for backwards compatibility. The use of keys (e.g. `telegram[obis_references.CURRENT_ELECTRICITY_USAGE]`) is deprecated.

Below are some examples on how to get the meter data. Alternatively check out the following unit test for a complete example: TelegramParserV5Test.test_parse

.. code-block:: python

    # Print contents of all available values
    # See dsmr_parser.obis_name_mapping for all readable telegram values.
    # The available values differ per DSMR version and meter.
    print(telegram)
    # P1_MESSAGE_HEADER: 	        42 [None]
    # P1_MESSAGE_TIMESTAMP: 	    2016-11-13 19:57:57+00:00 [None]
    # EQUIPMENT_IDENTIFIER: 	    3960221976967177082151037881335713 [None]
    # ELECTRICITY_USED_TARIFF_1:    1581.123 [kWh]
    # etc.

    # Example to get current electricity usage
    print(telegram.CURRENT_ELECTRICITY_USAGE)  # <dsmr_parser.objects.CosemObject at 0x7f5e98ae5ac8>
    print(telegram.CURRENT_ELECTRICITY_USAGE.value)  # Decimal('2.027')
    print(telegram.CURRENT_ELECTRICITY_USAGE.unit)  # 'kW'

    # All Mbus device readings like gas meters and water meters can be retrieved as follows. This
    # returns a list of MbusDevice objects:
    mbus_devices = telegram.MBUS_DEVICES

    # A specific MbusDevice based on the channel it's connected to, can be retrieved as follows:
    mbus_device = telegram.get_mbus_device_by_channel(1)
    print(mbus_device.DEVICE_TYPE.value)  # 3
    print(mbus_device.EQUIPMENT_IDENTIFIER_GAS.value)  # '4730303339303031393336393930363139'
    print(mbus_device.HOURLY_GAS_METER_READING.value)  # Decimal('246.138')

    # DEPRECATED: the dictionary approach of getting the values by key or `.items()' or '.get() is deprecated
    telegram[obis_references.CURRENT_ELECTRICITY_USAGE]


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
