import datetime

import pytz

# TODO : Use system timezone
# Preload timezone to avoid loading in event loop later
local_tz = pytz.timezone('Europe/Amsterdam')


def timestamp(value):
    try:
        naive_datetime = datetime.datetime.strptime(value[:-1], '%y%m%d%H%M%S')
    except ValueError:
        return None

    # Timestamp has the following format:
    # YYMMDDhhmmssX
    # ASCII presentation of Time stamp with
    # Year, Month, Day, Hour, Minute, Second,
    # and an indication whether DST is active
    # (X=S) or DST is not active (X=W)
    if len(value) == 13:
        is_dst = value[12] == 'S'  # assume format 160322150000W
    else:
        is_dst = False

    localized_datetime = local_tz.localize(naive_datetime, is_dst=is_dst)

    return localized_datetime.astimezone(pytz.utc)
