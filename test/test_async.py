"""Test async read/parse."""

import pytest
import asyncio
from dsmr_parser.serial import AsyncSerialReader, SERIAL_SETTINGS_V2_2
from dsmr_parser.obis_references import CURRENT_ELECTRICITY_USAGE, GAS_METER_READING
from dsmr_parser import telegram_specifications

TELEGRAM_V2_2 = [
    "/ISk5\2MT382-1004",
    "",
    "0-0:96.1.1(00000000000000)",
    "1-0:1.8.1(00001.001*kWh)",
    "1-0:1.8.2(00001.001*kWh)",
    "1-0:2.8.1(00001.001*kWh)",
    "1-0:2.8.2(00001.001*kWh)",
    "0-0:96.14.0(0001)",
    "1-0:1.7.0(0001.01*kW)",
    "1-0:2.7.0(0000.00*kW)",
    "0-0:17.0.0(0999.00*kW)",
    "0-0:96.3.10(1)",
    "0-0:96.13.1()",
    "0-0:96.13.0()",
    "0-1:24.1.0(3)",
    "0-1:96.1.0(000000000000)",
    "0-1:24.3.0(161107190000)(00)(60)(1)(0-1:24.2.1)(m3)",
    "(00001.001)",
    "0-1:24.4.0(1)",
    "!",
]


@pytest.mark.asyncio
def test_async_read(event_loop, mocker):
    """Test async read and parse."""

    mock_open_serial_connection = mocker.patch('serial_asyncio.open_serial_connection')
    mock_open_serial_connection.return_value = (mocker.stub(), None)

    queue = asyncio.Queue()

    serial_reader = AsyncSerialReader(
        device='/dev/ttyUSB0',
        serial_settings=SERIAL_SETTINGS_V2_2,
        telegram_specification=telegram_specifications.V2_2,
    )

    event_loop.run_until_complete(serial_reader.read(queue))

    assert not queue.get_nowait()

    result = yield from queue.get()

    assert float(result[CURRENT_ELECTRICITY_USAGE].value) == 1.01
    assert result[CURRENT_ELECTRICITY_USAGE].unit == 'kW'
    assert float(result[GAS_METER_READING].value) == 1.001
    assert result[GAS_METER_READING].unit == 'm3'
