DSMR Parser
===========

.. image:: https://img.shields.io/pypi/v/dsmr-parser.svg
    :target: https://pypi.python.org/pypi/dsmr-parser

.. image:: https://travis-ci.org/ndokter/dsmr_parser.svg?branch=master
    :target: https://travis-ci.org/ndokter/dsmr_parser

A library for parsing Dutch Smart Meter Requirements (DSMR) telegram data. It
also includes a serial client to directly read and parse smart meter data.


Features
--------

DSMR Parser currently supports DSMR versions 2.2 and 4.x. It has been tested with Python 3.4 and 3.5.


Examples
--------

Using the serial reader to connect to your smart meter and parse it's telegrams:

.. code-block:: python

    from dsmr_parser import telegram_specifications
    from dsmr_parser import obis_references
    from dsmr_parser.serial import SerialReader, SERIAL_SETTINGS_V4

    serial_reader = SerialReader(
        device='/dev/ttyUSB0',
        serial_settings=SERIAL_SETTINGS_V4,
        telegram_specification=telegram_specifications.V4
    )

    for telegram in serial_reader.read():

        # The telegram message timestamp.
        message_datetime = telegram[obis_references.P1_MESSAGE_TIMESTAMP]

        # Using the active tariff to determine the electricity being used and
        # delivered for the right tariff.
        tariff = telegram[obis_references.ELECTRICITY_ACTIVE_TARIFF]
        tariff = int(tariff.value)

        electricity_used_total \
            = telegram[obis_references.ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
        electricity_delivered_total = \
            telegram[obis_referencesELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]

        gas_reading = telegram[obis_references.HOURLY_GAS_METER_READING]

        # See dsmr_reader.obis_references for all readable telegram values.


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
