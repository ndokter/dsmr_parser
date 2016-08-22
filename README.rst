DSMR Parser
===========

A library for parsing Dutch Smart Meter Requirements (DSMR) telegram data. It
also includes a serial client to directly read and parse smart meter data.


Features
--------

DSMR Parser currently supports DSMR version 4 and is tested with Python 3.5


Examples
--------

Using the serial reader to connect to your smart meter and parse it's telegrams:

.. code-block:: python

    from dsmr_parser import telegram_specifications
    from dsmr_parser.obis_references import P1_MESSAGE_TIMESTAMP
    from dsmr_parser.serial import SerialReader, SERIAL_SETTINGS_V4

    serial_reader = SerialReader(
        device='/dev/ttyUSB0',
        serial_settings=SERIAL_SETTINGS_V4,
        telegram_specification=telegram_specifications.V4
    )

    for telegram in serial_reader.read():

        # The telegram message timestamp.
        message_datetime = telegram[P1_MESSAGE_TIMESTAMP]

        # Using the active tariff to determine the electricity being used and
        # delivered for the right tariff.
        tariff = telegram[ELECTRICITY_ACTIVE_TARIFF]
        tariff = int(tariff.value)

        electricity_used_total \
            = telegram[ELECTRICITY_USED_TARIFF_ALL[tariff - 1]]
        electricity_delivered_total = \
            telegram[ELECTRICITY_DELIVERED_TARIFF_ALL[tariff - 1]]

        gas_reading = telegram[HOURLY_GAS_METER_READING]

        # See dsmr_reader.obis_references for all readable telegram values.


Installation
------------

To install DSMR Parser:

.. code-block:: bash

    $ pip install dsmr-parser


TODO
----

- add unit tests
- verify telegram checksum
- improve ease of use
