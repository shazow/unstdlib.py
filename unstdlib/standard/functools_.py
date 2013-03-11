from functools import wraps

from list_ import iterate_items


__all__ = [
    'memoized', 'memoized_property', 'assert_hashable',
]


def assert_hashable(*args, **kw):
    """ Verify that each argument is hashable.

    Passes silently if successful. Raises descriptive TypeError otherwise.

    Example::

        >>> assert_hashable(1, 'foo', bar='baz')
        >>> assert_hashable(1, [], baz='baz')
        Traceback (most recent call last):
          ...
        TypeError: Argument in position 1 is not hashable: []
        >>> assert_hashable(1, 'foo', bar=[])
        Traceback (most recent call last):
          ...
        TypeError: Keyword argument 'bar' is not hashable: []
    """
    try:
        for i, arg in enumerate(args):
            hash(arg)
    except TypeError:
        raise TypeError('Argument in position %d is not hashable: %r' % (i, arg))
    try:
        for key, val in iterate_items(kw):
            hash(val)
    except TypeError:
        raise TypeError('Keyword argument %r is not hashable: %r' % (key, val))


def memoized(fn=None, cache=None):
    """ Memoize a function into an optionally-specificed cache container.

    If the `cache` container is not specified, then the instance container is
    accessible from the wrapped function's `memoize_cache` property.

    Example::

        >>> @memoized
        ... def foo(bar):
        ...   print "Not cached."
        >>> foo(1)
        Not cached.
        >>> foo(1)
        >>> foo(2)
        Not cached.

    Example with a specific cache container (in this case, the
    ``RecentlyUsedContainer``, which will only store the ``maxsize`` most
    recently accessed items)::

        >>> from unstdlib.standard.collections_ import RecentlyUsedContainer
        >>> lru_container = RecentlyUsedContainer(maxsize=2)
        >>> @memoized(cache=lru_container)
        ... def baz(x):
        ...   print "Not cached."
        >>> baz(1)
        Not cached.
        >>> baz(1)
        >>> baz(2)
        Not cached.
        >>> baz(3)
        Not cached.
        >>> baz(2)
        >>> baz(1)
        Not cached.
        >>> # Notice that the '2' key remains, but the '1' key was evicted from
        >>> # the cache.
    """
    if fn:
        # This is a hack to support both @memoize and @memoize(...)
        return memoized(cache=cache)(fn)

    if cache is None:
        cache = {}

    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kw):
            key = (args, tuple(sorted(kw.items())))

            try:
                is_cached = key in cache
            except TypeError, e:
                # Re-raise a more descriptive error if it's a hashing problem.
                assert_hashable(*args, **kw)
                # If it hasn't raised by now, then something else is going on,
                # raise it. (This shouldn't happen.)
                raise e

            if not is_cached:
                cache[key] = fn(*args, **kw)
            return cache[key]

        wrapped.memoize_cache = cache
        return wrapped

    return decorator


# `memoized_property` is lovingly borrowed from @zzzeek, with permission:
#   https://twitter.com/zzzeek/status/310503354268790784
class memoized_property(object):
    """ A read-only @property that is only evaluated once. """
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
