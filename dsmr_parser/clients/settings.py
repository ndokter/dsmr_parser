import serialx


SERIAL_SETTINGS_V2_2 = {
    'baudrate': 9600,
    'bytesize': serialx.SEVENBITS,
    'parity': serialx.PARITY_EVEN,
    'stopbits': serialx.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}

SERIAL_SETTINGS_V4 = {
    'baudrate': 115200,
    'bytesize': serialx.SEVENBITS,
    'parity': serialx.PARITY_EVEN,
    'stopbits': serialx.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}

SERIAL_SETTINGS_V5 = {
    'baudrate': 115200,
    'bytesize': serialx.EIGHTBITS,
    'parity': serialx.PARITY_NONE,
    'stopbits': serialx.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}
