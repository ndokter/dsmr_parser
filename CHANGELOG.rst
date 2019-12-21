Change Log
----------

**0.17** (2019-12-21)

- Add a true telegram object (`pull request #40 <https://github.com/ndokter/dsmr_parser/pull/40>`_).

**0.16** (2019-12-21)

- Add support for Belgian and Smarty meters (`pull request #44 <https://github.com/ndokter/dsmr_parser/pull/44>`_).

**0.15** (2019-12-12)

- Fixed asyncio loop issue (`pull request #43 <https://github.com/ndokter/dsmr_parser/pull/43>`_).

**0.14** (2019-10-08)

- Changed serial reading to reduce CPU usage (`pull request #37 <https://github.com/ndokter/dsmr_parser/pull/37>`_).

**0.13** (2019-03-04)

- Fix DSMR v5.0 serial settings which were not used (`pull request #33 <https://github.com/ndokter/dsmr_parser/pull/33>`_).

**0.12** (2018-09-23)

- Add serial settings for DSMR v5.0 (`pull request #31 <https://github.com/ndokter/dsmr_parser/pull/31>`_).
- Lux-creos-obis-1.8.0 (`pull request #32 <https://github.com/ndokter/dsmr_parser/pull/32>`_). 

**0.11** (2017-09-18)

- NULL value fix in checksum (`pull request #26 <https://github.com/ndokter/dsmr_parser/pull/26>`_)

**0.10** (2017-06-05)

- bugix: don't force full telegram signatures (`pull request #25 <https://github.com/ndokter/dsmr_parser/pull/25>`_)
- removed unused code for automatic telegram detection as this needs reworking after the fix mentioned above
- InvalidChecksumError's are logged as warning instead of error

**0.9** (2017-05-12)

- added DSMR v5 serial settings

**0.8** (2017-01-26)

- added support for DSMR v3
- added support for DSMR v5

**IMPORTANT: this release has the following backwards incompatible changes:**

- Removed TelegramParserV2_2 in favor of TelegramParser
- Removed TelegramParserV4 in favor of TelegramParser

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
