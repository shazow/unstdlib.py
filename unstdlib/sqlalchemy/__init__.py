from itertools import count


__all__ = ['enumerate_query_by_limit']


def enumerate_query_by_limit(q, limit=1000):
    """
    Enumerate over SQLAlchemy query object ``q`` and yield results in batches of
    size ``limit`` using limit and offset.
    """
    for offset in count(0, limit):
        r = q.offset(offset).limit(limit).all()
        yield r
        if len(r) < limit:
            break
