import datetime
from datetime import timezone
import dateutil.parser

def timestamp(value):

    # P1 Companion Standard v4.2.2 final
    # see 5.4 Representation of COSEM objects
    # YYMMDDhhmmssX, (X=S) or DST is not active (X=W).

    if len(value) == 13:
        is_dst = value[12] == 'S'
    else:
        # not specified
        is_dst = False

    # create iso8601 format with as little help as possible
    # 2018-07-11T08:13:33+00:00
    iso8601_value = "20{year}-{month}-{day}T{hour}:{minute}:{second}+{offset}:00".format(
        year=value[0:2],
        month=value[2:4],
        day=value[4:6],
        hour=value[6:8],
        minute=value[8:10],
        second=value[10:12],
        offset=('02' if is_dst else '01')
    )

    d = dateutil.parser.parse(iso8601_value)

    return d.astimezone(timezone.utc)
