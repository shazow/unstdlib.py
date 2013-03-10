def _create_memoize_decorator(cache):
    def decorator(fn):
        def wrapped(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in cache:
                cache[key] = fn(*args, **kwargs)
            return cache[key]
        return wrapped
    return decorator


def memoized_into(cache=None):
    """ Memoize a function into an optionally-specificed cache container.

    Example::

        >>> cache_container = {}
        >>> @memoized_into(cache_container)
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
    """
    if cache is None:
        cache = {}

    return _create_memoize_decorator(cache)


def memoized(fn):
    """ A shortcut for :method:`memoized_into` which can be applied without the
    vulgar parenthesis.

    Example::

        >>> @memoized
        ... def foo(bar=None):
        ...   print "Not cached."
        >>> foo()
        Not cached.
        >>> foo()
        >>> foo(1)
        Not cached.
    """
    return memoized_into()(fn)


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
