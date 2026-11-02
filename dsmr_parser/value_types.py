from __future__ import annotations

from datetime import datetime, timezone
from functools import partial
from typing import Callable
from zoneinfo import ZoneInfo


_SYSTEM_TZ = ZoneInfo("Europe/Amsterdam")


def timestamp(value: str, tz: ZoneInfo = _SYSTEM_TZ) -> datetime | None:
    """
    Parse a DSMR-style timestamp string and convert it to UTC.

    Expected format:
        YYMMDDhhmmssX

    Where:
        - YY   : 2-digit year
        - MM   : month
        - DD   : day
        - hh   : hour
        - mm   : minute
        - ss   : second
        - X    : DST indicator
                 'S' = summer time (DST active)
                 'W' = winter time (standard time)

    Example:
        "160322150000W"

    Args:
        value: Timestamp string in DSMR format.
        tz: Time zone the meter clock runs in (default: Europe/Amsterdam).

    Returns:
        A timezone-aware datetime in UTC if parsing succeeds,
        otherwise None.
    """
    if not isinstance(value, str):
        return None

    if len(value) not in (12, 13):
        return None

    try:
        naive_dt = datetime.strptime(value[:12], "%y%m%d%H%M%S")
    except ValueError:
        return None

    # Determine DST fold handling
    # fold=1 represents the second occurrence (after DST switch)
    fold = 0
    if len(value) == 13:
        dst_flag = value[12]
        if dst_flag not in {"S", "W"}:
            return None

        # When DST is NOT active (W) during ambiguous hour,
        # we must use fold=1 to indicate winter time.
        if dst_flag == "W":
            fold = 1

    localized_datetime = naive_dt.replace(tzinfo=tz, fold=fold)

    return localized_datetime.astimezone(timezone.utc)


def timestamp_in(tz_name: str) -> Callable[[str], datetime | None]:
    """
    Return a timestamp parser for meters whose clock runs in a time zone
    other than the default, e.g. timestamp_in('Europe/Dublin').
    """
    return partial(timestamp, tz=ZoneInfo(tz_name))
