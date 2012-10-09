from itertools import chain
from functools import wraps
from collections import defaultdict


__all__ = [
    'groupby_count',
    'iterate', 'is_iterable', 'iterate_chunks', 'iterate_flatten',
    'listify',
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


def is_iterable(maybe_iter, unless=(basestring, dict)):
    """
    Return whether ``maybe_iter`` is an iterable, unless it's an instance of one
    of the base class, or tuple of base classes, given in ``unless``.

    >>> is_iterable('foo')
    False
    >>> is_iterable(['foo'])
    True
    >>> is_iterable(['foo'], unless=list)
    False
    >>> is_iterable(xrange(5))
    True
    """
    try:
        iter(maybe_iter)
    except TypeError:
        return False
    return not isinstance(maybe_iter, unless)


def iterate(maybe_iter, unless=(basestring, dict)):
    """
    Always return an iterable.

    Returns ``maybe_iter`` if it is an iterable, otherwise it returns a single
    element iterable containing ``maybe_iter``. By default, strings and dicts
    are treated as non-iterable. This can be overridden by passing in a type
    or tuple of types for ``unless``.

    :param maybe_iter:
        A value to return as an iterable.

    :param unless:
        A type or tuple of types (same as ``isinstance``) to be treated as
        non-iterable.

    Example::

    >>> iterate('foo')
    ['foo']
    >>> iterate(['foo'])
    ['foo']
    >>> iterate(['foo'], unless=list)
    [['foo']]
    >>> list(iterate(xrange(5)))
    [0, 1, 2, 3, 4]
    """
    if is_iterable(maybe_iter, unless=unless):
        return maybe_iter
    return [maybe_iter]


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


def listify(fn=None, wrapper=list):
    """
    A decorator which wraps a function's return value in ``list(...)``.

    Useful when an algorithm can be expressed more cleanly as a generator but
    the function should return an list.

    Example::

        >>> @listify
        ... def get_lengths(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths(["spam", "eggs"])
        [4, 4]
        >>>
        >>> @listify(wrapper=tuple)
        ... def get_lengths_tuple(iterable):
        ...     for i in iterable:
        ...         yield len(i)
        >>> get_lengths_tuple(["foo", "bar"])
        (3, 3)
    """
    def listify_return(fn):
        @wraps(fn)
        def listify_helper(*args, **kwargs):
            return wrapper(fn(*args, **kwargs))
        return listify_helper
    if fn is None:
        return listify_return
    return listify_return(fn)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
