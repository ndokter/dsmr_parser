from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


_SYSTEM_TZ = ZoneInfo("Europe/Amsterdam")


def timestamp(value: str) -> datetime | None:
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

    localized_datetime = naive_dt.replace(tzinfo=_SYSTEM_TZ, fold=fold)

    return localized_datetime.astimezone(timezone.utc)
