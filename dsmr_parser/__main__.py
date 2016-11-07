import argparse
from dsmr_parser.serial import SERIAL_SETTINGS_V2_2, SERIAL_SETTINGS_V4, SerialReader
from dsmr_parser import telegram_specifications


def console():
    """Output DSMR data to console."""

    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument('--device', default='/dev/ttyUSB0',
                        help='port to read DSMR data from')
    parser.add_argument('--version', default='2.2', choices=['2.2', '4'],
                        help='DSMR version (2.2, 4)')

    args = parser.parse_args()

    settings = {
        '2.2': (SERIAL_SETTINGS_V2_2, telegram_specifications.V2_2),
        '4': (SERIAL_SETTINGS_V4, telegram_specifications.V4),
    }

    serial_reader = SerialReader(
        device=args.device,
        serial_settings=settings[args.version][0],
        telegram_specification=settings[args.version][1],
    )

    for telegram in serial_reader.read():
        for obiref, obj in telegram.items():
            if obj:
                print(obj.value, obj.unit)
        print()
