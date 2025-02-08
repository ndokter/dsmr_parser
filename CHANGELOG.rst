Change Log
----------

**1.4.3** (2025-02-08)

- Don't throw an error when string can't be decoded to ascii (`PR #170 <https://github.com/ndokter/dsmr_parser/pull/170>`_ by `ekaats <https://github.com/ekaats>`_)

**1.4.2** (2024-07-14)

- Bump Github Actions to latest versions in favor of Node deprecations (`PR #159 <https://github.com/ndokter/dsmr_parser/pull/159>`_ by `dennissiemensma <https://github.com/dennissiemensma>`_)
- Swap pyserial-asyncio for pyserial-asyncio-fast (`PR #158 <https://github.com/ndokter/dsmr_parser/pull/158>`_ by `bdraco <https://github.com/bdraco>`_)

**1.4.1** (2024-06-04)

- Avoid loading timezone at runtime (`PR #157 <https://github.com/ndokter/dsmr_parser/pull/157>`_ by `elupus <https://github.com/elupus>`_)

**1.4.0** (2024-03-12)

- Mbus alt (`PR #142 <https://github.com/ndokter/dsmr_parser/pull/142>`_ by `dupondje <https://github.com/dupondje>`_)
- Q3D add CURRENT_ELECTRICITY_DELIVERY (`PR #149 <https://github.com/ndokter/dsmr_parser/pull/149>`_ by `Aeroid <https://github.com/Aeroid>`_)
- Copy head_parsers list on construct. (`PR #150 <https://github.com/ndokter/dsmr_parser/pull/150>`_ by `dupondje <https://github.com/dupondje>`_)

**1.3.2** (2024-01-29)

- Fix unit test for pyton 3.12 (`PR #148 <https://github.com/ndokter/dsmr_parser/pull/148>`_ by `ndokter <https://github.com/ndokter>`_)

**1.3.1** (2023-11-06)

- Fix parsing peak usage with invalid timestamps (`PR #143 <https://github.com/ndokter/dsmr_parser/pull/143>`_ by `dupondje <https://github.com/dupondje>`_)

**1.3.0** (2023-08-01)

- added E.ON Hungary; refactored DSMR specifications to fix obis reference conflicts (`PR #137 <https://github.com/ndokter/dsmr_parser/pull/137>`_ by `balazs92117 <https://github.com/balazs92117>`_)

**1.2.4** (2023-07-11)

- EQUIPMENT IDENTIFIER is wrong for Fluvius meters when other mbus devices are present (`PR #133 <https://github.com/ndokter/dsmr_parser/pull/133>`_ by `ejpalacios <https://github.com/ejpalacios>`_)


**1.2.3** (2023-04-18)

- Fix parsing tests and line start matching (`PR #132 <https://github.com/ndokter/dsmr_parser/pull/132>`_ by `dupondje <https://github.com/dupondje>`_)

**1.2.2** (2023-04-12)

- Improve performance. Thanks to `ejpalacios <https://github.com/bdraco>`_ (`PR #130 <https://github.com/ndokter/dsmr_parser/pull/130>`_ by `ndokter <https://github.com/ndokter>`_)

**1.2.1** (2023-04-05)

- Bug/duplicate index BELGIUM_MAXIMUM_DEMAND_13_MONTHS (`PR #129 <https://github.com/ndokter/dsmr_parser/pull/129>`_ by `ejpalacios <https://github.com/ejpalacios>`_)

**1.2.0** (2023-02-18)

- Improved gas meter (mbus devices) support and replaced Telegram dictionary with backwards compatible object (`PR #121 <https://github.com/ndokter/dsmr_parser/pull/121>`_ by `ndokter <https://github.com/ndokter>`_)
- Fix parsing with invalid timestamps (`PR #125 <https://github.com/ndokter/dsmr_parser/pull/125>`_ by `dupondje <https://github.com/dupondje>`_)
- Add Iskra IE.x meters specification (`PR #126 <https://github.com/ndokter/dsmr_parser/pull/126>`_ by `jchevalier7 <https://github.com/jchevalier7>`_)

**1.1.0** (2023-02-08)

- Add instantaneous reactive power + fixed swapped reactive total import export (`PR #124 <https://github.com/ndokter/dsmr_parser/pull/124>`_ by `yada75 <https://github.com/yada75>`_)

**1.0.0** (2022-12-22)

- switched to new numbering scheme https://semver.org/
- Added support for Python 3.11 and dropped support for Python 3.6 (`PR #112 <https://github.com/ndokter/dsmr_parser/pull/112>`_ by `dennissiemensma <https://github.com/dennissiemensma>`_)
- Add support for Fluvius V1.7.1 DSMR messages (`PR #110 <https://github.com/ndokter/dsmr_parser/pull/113>`_ by `dupondje <https://github.com/dupondje>`_)

**0.34** (2022-10-19)

- Adds support for the Sagemcom T210-D-r smart meter (`PR #110 <https://github.com/ndokter/dsmr_parser/pull/110>`_).

**0.33** (2022-04-20)

- Test Python 3.10 in CI + legacy badge fix (`PR #105 <https://github.com/ndokter/dsmr_parser/pull/105>`_).
- Update telegram_specifications.py (`PR #106 <https://github.com/ndokter/dsmr_parser/pull/106>`_).
- Improve compatiblity with Belgian standard (`PR #107 <https://github.com/ndokter/dsmr_parser/pull/107>`_).
- Improve documentation asyncio (`PR #63 <https://github.com/ndokter/dsmr_parser/pull/63>`_).

**0.32** (2022-01-04)

- Support DSMR data read via RFXtrx with integrated P1 reader (`PR #98 <https://github.com/ndokter/dsmr_parser/pull/98>`_).

**0.31** (2021-11-21)

- Support for (German) EasyMeter Q3D using COM-1 Ethernet Gateway (`PR #92 <https://github.com/ndokter/dsmr_parser/pull/92>`_).

**0.30** (2021-08-18)

- Add support for Swedish smart meters (`PR #86 <https://github.com/ndokter/dsmr_parser/pull/86>`_).

**0.29** (2021-04-18)

- Add value and unit properties to ProfileGenericObject to make sure that code like iterators that rely on that do not break (`PR #71 <https://github.com/ndokter/dsmr_parser/pull/71>`_).
Remove deprecated asyncio coroutine decorator (`PR #76 <https://github.com/ndokter/dsmr_parser/pull/76>`_).

**0.28** (2021-02-21)

- Optional keep alive monitoring for TCP/IP connections (`PR #73 <https://github.com/ndokter/dsmr_parser/pull/73>`_).
- Catch parse errors in TelegramParser, ignore lines that can not be parsed (`PR #74 <https://github.com/ndokter/dsmr_parser/pull/74>`_).

**0.27** (2020-12-24)

- fix for empty parentheses in ProfileGenericParser (redone) (`PR #69 <https://github.com/ndokter/dsmr_parser/pull/69>`_).

**0.26** (2020-12-15)

- reverted fix for empty parentheses in ProfileGenericParser (`PR #68 <https://github.com/ndokter/dsmr_parser/pull/68>`_).

**0.25** (2020-12-14)

- fix for empty parentheses in ProfileGenericParser (`PR #57 <https://github.com/ndokter/dsmr_parser/pull/57>`_).

**0.24** (2020-11-27)

- Add Luxembourg equipment identifier (`PR #62 <https://github.com/ndokter/dsmr_parser/pull/62>`_).

**0.23** (2020-11-07)

- Resolved issue with x-x:24.3.0 where it contains non-integer character (`PR #61 <https://github.com/ndokter/dsmr_parser/pull/61>`_).
- Tests are not installed anymore (`PR #59 <https://github.com/ndokter/dsmr_parser/pull/59>`_).
- Example telegram improvement (`PR #58 <https://github.com/ndokter/dsmr_parser/pull/58>`_).

**0.22** (2020-08-23)

- CRC check speed is improved
- Exception info improvement

**0.21** (2020-05-25)

- All objects can produce a json serialization of their state.

**0.20** (2020-05-12)

- All objects can now print their values
- Add parser + object for generic profile

**0.19** (2020-05-03)

- Add following missing elements to telegram specification v4:
    - SHORT_POWER_FAILURE_COUNT,
    - INSTANTANEOUS_CURRENT_L1,
    - INSTANTANEOUS_CURRENT_L2,
    - INSTANTANEOUS_CURRENT_L3
- Add missing tests + fix small test bugs
- Complete telegram object v4 parse test

**0.18** (2020-01-28)

- PyCRC replacement (`PR #48 <https://github.com/ndokter/dsmr_parser/pull/48>`_).

**0.17** (2019-12-21)

- Add a true telegram object (`PR #40 <https://github.com/ndokter/dsmr_parser/pull/40>`_).

**0.16** (2019-12-21)

- Add support for Belgian and Smarty meters (`PR #44 <https://github.com/ndokter/dsmr_parser/pull/44>`_).

**0.15** (2019-12-12)

- Fixed asyncio loop issue (`PR #43 <https://github.com/ndokter/dsmr_parser/pull/43>`_).

**0.14** (2019-10-08)

- Changed serial reading to reduce CPU usage (`PR #37 <https://github.com/ndokter/dsmr_parser/pull/37>`_).

**0.13** (2019-03-04)

- Fix DSMR v5.0 serial settings which were not used (`PR #33 <https://github.com/ndokter/dsmr_parser/pull/33>`_).

**0.12** (2018-09-23)

- Add serial settings for DSMR v5.0 (`PR #31 <https://github.com/ndokter/dsmr_parser/pull/31>`_).
- Lux-creos-obis-1.8.0 (`PR #32 <https://github.com/ndokter/dsmr_parser/pull/32>`_). 

**0.11** (2017-09-18)

- NULL value fix in checksum (`PR #26 <https://github.com/ndokter/dsmr_parser/pull/26>`_)

**0.10** (2017-06-05)

- bugfix: don't force full telegram signatures (`PR #25 <https://github.com/ndokter/dsmr_parser/pull/25>`_)
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

- Internal refactoring related to the way clients feed their data into the parse module. Clients can now supply the telegram data in single characters, lines (which was common) or complete telegram strings. (`PR #17 <https://github.com/ndokter/dsmr_parser/pull/17>`_)

**IMPORTANT: this release has the following backwards incompatible changes:**

- Client related imports from dsmr_parser.serial and dsmr_parser.protocol have been moved to dsmr_parser.clients (import these from the clients/__init__.py module)
- The .parse() method of TelegramParser, TelegramParserV2_2, TelegramParserV4 now accepts a string containing the entire telegram (including \r\n characters) and not a list


**0.6** (2017-01-04)

- Fixed bug in CRC checksum verification for the asyncio client (`PR #15 <https://github.com/ndokter/dsmr_parser/pull/15>`_)
- Support added for TCP connections using the asyncio client (`PR #12 <https://github.com/ndokter/dsmr_parser/pull/12/>`_)

**0.5** (2016-12-29)

- CRC checksum verification for DSMR v4 telegrams (`issue #10 <https://github.com/ndokter/dsmr_parser/issues/10>`_)

**0.4** (2016-11-21)

- DSMR v2.2 serial settings now uses parity serial.EVEN by default (`PR #5 <https://github.com/ndokter/dsmr_parser/pull/5>`_)
- improved asyncio reader and improve it's error handling (`PR #8 <https://github.com/ndokter/dsmr_parser/pull/8>`_)

**0.3** (2016-11-12)

- asyncio reader for non-blocking reads (`PR #3 <https://github.com/ndokter/dsmr_parser/pull/3>`_)

**0.2** (2016-11-08)

- support for DMSR version 2.2 (`PR #2 <https://github.com/ndokter/dsmr_parser/pull/2>`_)

**0.1** (2016-08-22)

- initial version with a serial reader and support for DSMR version 4.x
