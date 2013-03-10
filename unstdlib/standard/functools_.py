from functools import wraps


__all__ = [
    'memoized', 'memoized_property',
]


def memoized(fn=None, cache=None):
    """ Memoize a function into an optionally-specificed cache container.

    If the `cache` container is not specified, then the instance container is
    accessible from the wrapped function's `memoize_cache` property.

    Example::

        >>> @memoized
        ... def foo(bar=None):
        ...   print "Not cached."
        >>> foo()
        Not cached.
        >>> foo()
        >>> foo(1)
        Not cached.
        >>> foo(1)
        >>> foo()
        >>> foo(2)
        Not cached.

    Example with a specific cache container::

        >>> cache_container = {}
        >>> @memoized(cache=cache_container)
        ... def baz(quux=None):
        ...   print "Not cached."
        >>> baz(quux=42)
        Not cached.
        >>> baz(quux=42)
        >>> cache_container.clear()
        >>> baz(quux=42)
        Not cached.
    """
    if fn:
        # This is a hack to support both @memoize and @memoize(...)
        return memoized(cache=cache)(fn)

    if cache is None:
        cache = {}

    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in cache:
                cache[key] = fn(*args, **kwargs)
            return cache[key]
        wrapped.memoize_cache = cache
        return wrapped
    return decorator


# `memoized_property` is lovingly borrowed from @zzzeek, with permission:
#   https://twitter.com/zzzeek/status/310503354268790784
class memoized_property(object):
    """A read-only @property that is only evaluated once."""
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
