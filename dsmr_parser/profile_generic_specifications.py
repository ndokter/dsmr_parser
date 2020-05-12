from dsmr_parser.parsers import ValueParser, MBusParser
from dsmr_parser.value_types import timestamp

FAILURE_EVENT = r'0-0\:96\.7\.19'

V4 = {
    'objects': {
        FAILURE_EVENT:  MBusParser(
            ValueParser(timestamp),
            ValueParser(int)
        )
    }

}
