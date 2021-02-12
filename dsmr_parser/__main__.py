from functools import partial
import argparse
import asyncio
import logging

from dsmr_parser.clients import create_dsmr_reader, create_tcp_dsmr_reader


def console():
    """Output DSMR data to console."""

    parser = argparse.ArgumentParser(description=console.__doc__)
    parser.add_argument('--device', default='/dev/ttyUSB0',
                        help='port to read DSMR data from')
    parser.add_argument('--host', default=None,
                        help='alternatively connect using TCP host.')
    parser.add_argument('--port', default=None,
                        help='TCP port to use for connection')
    parser.add_argument('--version', default='2.2', choices=['2.2', '4', '5', '5B', '5L'],
                        help='DSMR version (2.2, 4, 5, 5B, 5L)')
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

    # create tcp or serial connection depending on args
    if args.host and args.port:
        create_connection = partial(create_tcp_dsmr_reader,
                                    args.host, args.port, args.version,
                                    print_callback, loop=loop)
    else:
        create_connection = partial(create_dsmr_reader,
                                    args.device, args.version,
                                    print_callback, loop=loop)

    try:
        # connect and keep connected until interrupted by ctrl-c
        while True:
            # create serial or tcp connection
            conn = create_connection()
            transport, protocol = loop.run_until_complete(conn)
            # wait until connection it closed
            loop.run_until_complete(protocol.wait_closed())
            # wait 5 seconds before attempting reconnect
            loop.run_until_complete(asyncio.sleep(5))
    except KeyboardInterrupt:
        # cleanup connection after user initiated shutdown
        transport.close()
        loop.run_until_complete(asyncio.sleep(0))
    finally:
        loop.close()
