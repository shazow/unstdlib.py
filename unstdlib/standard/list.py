from itertools import chain
from collections import defaultdict


__all__ = [
    'groupby_count',
    'iterate_chunks', 'iterate_flatten',
]


def groupby_count(i, key=None, force_keys=None):
    """
    Example::

        [1,1,1,2,3] -> [(1,3),(2,1),(3,1)]
    """
    counter = defaultdict(lambda: 0)
    if not key:
        key = lambda o: o

    for k in i:
        counter[key(k)] += 1

    if force_keys:
        for k in force_keys:
            counter[k] += 0

    return counter.items()


def iterate_chunks(i, size=10):
    """
    Iterate over an iterator ``i`` in ``size`` chunks, yield chunks.
    Similar to pagination.

    Example::

        list(iterate_chunks([1,2,3,4], size=2)) -> [[1,2],[3,4]]
    """
    accumulator = []

    for n, i in enumerate(i):
        accumulator.append(i)
        if (n+1) % size == 0:
            yield accumulator
            accumulator = []

    if accumulator:
        yield accumulator


def iterate_flatten(q):
    """
    Flatten nested lists.

    Useful for flattening one-value tuple rows returned from a database query.

    Example::

        [("foo",), ("bar",)] -> ["foo", "bar"]

        [[1,2,3],[4,5,6]] -> [1,2,3,4,5,6]

    """

    return chain.from_iterable(q)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
