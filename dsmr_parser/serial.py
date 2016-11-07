import serial

from dsmr_parser.parsers import TelegramParser, TelegramParserV2_2

SERIAL_SETTINGS_V2_2 = {
    'baudrate': 9600,
    'bytesize': serial.SEVENBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}

SERIAL_SETTINGS_V4 = {
    'baudrate': 115200,
    'bytesize': serial.SEVENBITS,
    'parity': serial.PARITY_EVEN,
    'stopbits': serial.STOPBITS_ONE,
    'xonxoff': 0,
    'rtscts': 0,
    'timeout': 20
}


def is_start_of_telegram(line):
    return line.startswith('/')


def is_end_of_telegram(line):
    return line.startswith('!')


class SerialReader(object):

    def __init__(self, device, serial_settings, telegram_specification):
        self.serial_settings = serial_settings
        self.serial_settings['port'] = device

        if serial_settings is SERIAL_SETTINGS_V2_2:
            telegram_parser = TelegramParserV2_2
        else:
            telegram_parser = TelegramParser
        self.telegram_parser = telegram_parser(telegram_specification)

    def read(self):
        """
        Read complete DSMR telegram's from the serial interface and parse it
        into CosemObject's and MbusObject's

        :rtype dict
        """
        with serial.Serial(**self.serial_settings) as serial_handle:
            telegram = []

            while True:
                line = serial_handle.readline()
                line = line.decode('ascii')

                # Telegrams need to be complete because the values belong to a
                # particular reading and can also be related to eachother.
                if not telegram and not is_start_of_telegram(line):
                    continue

                telegram.append(line)

                if is_end_of_telegram(line):
                    yield self.telegram_parser.parse(telegram)
                    telegram = []
