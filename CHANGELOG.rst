Change Log
----------

**0.7** (2017-01-14)

- Internal refactoring related to the way clients feed their data into the parse module. Clients can now supply the telegram data in single characters, lines (which was common) or complete telegram strings. (`pull request #17 <https://github.com/ndokter/dsmr_parser/pull/17>`_)

**IMPORTANT: this release has the following backwards incompatible changes:**

- Client related imports from dsmr_parser.serial and dsmr_parser.protocol have been moved to dsmr_parser.clients (import these from the clients/__init__.py module)
- The .parse() method of TelegramParser, TelegramParserV2_2, TelegramParserV4 now accepts a string containing the entire telegram (including \r\n characters) and not a list


**0.6** (2017-01-04)

- Fixed bug in CRC checksum verification for the asyncio client (`pull request #15 <https://github.com/ndokter/dsmr_parser/pull/15>`_)
- Support added for TCP connections using the asyncio client (`pull request #12 <https://github.com/ndokter/dsmr_parser/pull/12/>`_)

**0.5** (2016-12-29)

- CRC checksum verification for DSMR v4 telegrams (`issue #10 <https://github.com/ndokter/dsmr_parser/issues/10>`_)

**0.4** (2016-11-21)

- DSMR v2.2 serial settings now uses parity serial.EVEN by default (`pull request #5 <https://github.com/ndokter/dsmr_parser/pull/5>`_)
- improved asyncio reader and improve it's error handling (`pull request #8 <https://github.com/ndokter/dsmr_parser/pull/8>`_)

**0.3** (2016-11-12)

- asyncio reader for non-blocking reads (`pull request #3 <https://github.com/ndokter/dsmr_parser/pull/3>`_)

**0.2** (2016-11-08)

- support for DMSR version 2.2 (`pull request #2 <https://github.com/ndokter/dsmr_parser/pull/2>`_)

**0.1** (2016-08-22)

- initial version with a serial reader and support for DSMR version 4.x
