import argparse
import asyncio
import logging

from .protocol import create_dsmr_reader


def console():
    """Output DSMR data to console."""

    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument('--device', default='/dev/ttyUSB0',
                        help='port to read DSMR data from')
    parser.add_argument('--version', default='2.2', choices=['2.2', '4'],
                        help='DSMR version (2.2, 4)')
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.ERROR
    logging.basicConfig(level=level)

    loop = asyncio.get_event_loop()

    def print_callback(telegram):
        """Callback that prints telegram values."""
        for obiref, obj in telegram.items():
            if obj:
                print(obj.value, obj.unit)
        print()

    conn = create_dsmr_reader(args.device, args.version, print_callback, loop=loop)

    loop.create_task(conn)
    loop.run_forever()
