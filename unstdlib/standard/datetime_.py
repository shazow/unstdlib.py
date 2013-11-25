import calendar
import datetime


__all__ = ['iterate_date', 'iterate_date_values', 'isoformat_as_datetime',
           'truncate_datetime', 'now', 'datetime_from_timestamp',
           'timestamp_from_datetime']


def iterate_date(start, stop=None, step=datetime.timedelta(days=1)):
    while not stop or start <= stop:
        yield start
        start += step


def iterate_date_values(d, start_date=None, stop_date=None, default=0):
    """
    Convert (date, value) sorted lists into contiguous value-per-day data sets. Great for sparklines.

    Example::

        [(datetime.date(2011, 1, 1), 1), (datetime.date(2011, 1, 4), 2)] -> [1, 0, 0, 2]

    """
    dataiter = iter(d)
    cur_day, cur_val = next(dataiter)

    start_date = start_date or cur_day

    while cur_day < start_date:
        cur_day, cur_val = next(dataiter)

    for d in iterate_date(start_date, stop_date):
        if d != cur_day:
            yield default
            continue

        yield cur_val
        try:
            cur_day, cur_val = next(dataiter)
        except StopIteration:
            if not stop_date:
                raise


def isoformat_as_datetime(s):
    """
    Convert a datetime.datetime.isoformat() string to a datetime.datetime() object.
    """
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')


def truncate_datetime(t, resolution):
    """
    Given a datetime ``t`` and a ``resolution``, flatten the precision beyond the given resolution.

    ``resolution`` can be one of: year, month, day, hour, minute, second, microsecond

    Example::

        >>> t = datetime.datetime(2000, 1, 2, 3, 4, 5, 6000) # Or, 2000-01-02 03:04:05.006000

        >>> truncate_datetime(t, 'day')
        datetime.datetime(2000, 1, 2, 0, 0)
        >>> _.isoformat()
        '2000-01-02T00:00:00'

        >>> truncate_datetime(t, 'minute')
        datetime.datetime(2000, 1, 2, 3, 4)
        >>> _.isoformat()
        '2000-01-02T03:04:00'

    """

    resolutions = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    if resolution not in resolutions:
        raise KeyError("Resolution is not valid: {0}".format(resolution))

    args = []
    for r in resolutions:
        args += [getattr(t, r)]
        if r == resolution:
            break

    return datetime.datetime(*args)

def to_timezone(dt, timezone):
    """
    Return an aware datetime which is ``dt`` converted to ``timezone``.

    If ``dt`` is naive, it is assumed to be UTC.

    For example, if ``dt`` is "06:00 UTC+0000" and ``timezone`` is "EDT-0400",
    then the result will be "02:00 EDT-0400".

    This method follows the guidelines in http://pytz.sourceforge.net/
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_UTC)
    return timezone.normalize(dt.astimezone(timezone))

def now(timezone=None):
    """
    Return a naive datetime object for the given ``timezone``. A ``timezone``
    is any pytz- like or datetime.tzinfo-like timezone object. If no timezone
    is given, then UTC is assumed.

    This method is best used with pytz installed::

        pip install pytz
    """
    d = datetime.datetime.utcnow()
    if not timezone:
        return d

    return to_timezone(d, timezone).replace(tzinfo=None)

def datetime_from_timestamp(timestamp):
    """
    Returns a naive datetime from ``timestamp``.

    >>> datetime_from_timestamp(1234.5)
    datetime.datetime(1970, 1, 1, 0, 20, 34, 500000)
    """
    return datetime.datetime.utcfromtimestamp(timestamp)

def timestamp_from_datetime(dt):
    """
    Returns a timestamp from datetime ``dt``.

    Note that timestamps are always UTC. If ``dt`` is aware, the resulting
    timestamp will correspond to the correct UTC time.

    >>> timestamp_from_datetime(datetime.datetime(1970, 1, 1, 0, 20, 34, 500000))
    1234.5
    """
    return calendar.timegm(dt.utctimetuple()) + (dt.microsecond / 1000000.0)

# Built-in timezone for when pytz isn't available:

_ZERO = datetime.timedelta(0)

class _UTC(datetime.tzinfo):
    """
    UTC implementation taken from Python's docs.

    Use only when pytz isn't available.
    """

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return _ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _ZERO


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
