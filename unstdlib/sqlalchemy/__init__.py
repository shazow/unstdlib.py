from itertools import count


__all__ = ['enumerate_query_by_limit']


def enumerate_query_by_limit(q, limit=1000):
    """
    Enumerate over SQLAlchemy query object ``q`` and yield individual results
    fetched in batches of size ``limit`` using SQL LIMIT and OFFSET.
    """
    for offset in count(0, limit):
        r = q.offset(offset).limit(limit).all()

        for row in r:
            yield row

        if len(r) < limit:
            break
