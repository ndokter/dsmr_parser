import datetime

import pytz


def timestamp(value):

    naive_datetime = datetime.datetime.strptime(value[:-1], '%y%m%d%H%M%S')
    is_dst = value[12] == 'S'  # assume format 160322150000W

    local_tz = pytz.timezone('Europe/Amsterdam')
    localized_datetime = local_tz.localize(naive_datetime, is_dst=is_dst)

    return localized_datetime.astimezone(pytz.utc)
