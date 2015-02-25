from functools import wraps, partial
import warnings

from .list_ import iterate_items


__all__ = [
    'memoized', 'memoized_property', 'memoized_method',
    'assert_hashable', 'deprecated',
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


def _memoized_call(fn, cache, *args, **kw):
    key = (args, tuple(sorted(kw.items())))

    try:
        is_cached = key in cache
    except TypeError as e:
        # Re-raise a more descriptive error if it's a hashing problem.
        assert_hashable(*args, **kw)
        # If it hasn't raised by now, then something else is going on,
        # raise it. (This shouldn't happen.)
        raise e

    if not is_cached:
        cache[key] = fn(*args, **kw)
    return cache[key]


def memoized(fn=None, cache=None):
    """ Memoize a function into an optionally-specificed cache container.

    If the `cache` container is not specified, then the instance container is
    accessible from the wrapped function's `memoize_cache` property.

    Example::

        >>> @memoized
        ... def foo(bar):
        ...   print("Not cached.")
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
        ...   print("Not cached.")
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
        wrapped = wraps(fn)(partial(_memoized_call, fn, cache))
        wrapped.memoize_cache = cache
        return wrapped

    return decorator


# `memoized_property` is lovingly borrowed from @zzzeek, with permission:
#   https://twitter.com/zzzeek/status/310503354268790784
class memoized_property(object):
    """ A read-only @property that is only evaluated once. """
    def __init__(self, fget, doc=None, name=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = name or fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result


def memoized_method(method=None, cache_factory=None):
    """ Memoize a class's method.

    Arguments are similar to to `memoized`, except that the cache container is
    specified with `cache_factory`: a function called with no arguments to
    create the caching container for the instance.

    Note that, unlike `memoized`, the result cache will be stored on the
    instance, so cached results will be deallocated along with the instance.

    Example::

        >>> class Person(object):
        ...     def __init__(self, name):
        ...         self._name = name
        ...     @memoized_method
        ...     def get_name(self):
        ...         print("Calling get_name on %r" %(self._name, ))
        ...         return self._name
        >>> shazow = Person("shazow")
        >>> shazow.get_name()
        Calling get_name on 'shazow'
        'shazow'
        >>> shazow.get_name()
        'shazow'
        >>> shazow._get_name_cache
        {((), ()): 'shazow'}

    Example with a specific cache container::

        >>> from unstdlib.standard.collections_ import RecentlyUsedContainer
        >>> class Foo(object):
        ...     @memoized_method(cache_factory=lambda: RecentlyUsedContainer(maxsize=2))
        ...     def add(self, a, b):
        ...         print("Calling add with %r and %r" %(a, b))
        ...         return a + b
        >>> foo = Foo()
        >>> foo.add(1, 1)
        Calling add with 1 and 1
        2
        >>> foo.add(1, 1)
        2
        >>> foo.add(2, 2)
        Calling add with 2 and 2
        4
        >>> foo.add(3, 3)
        Calling add with 3 and 3
        6
        >>> foo.add(1, 1)
        Calling add with 1 and 1
        2
    """

    if method is None:
        return lambda f: memoized_method(f, cache_factory=cache_factory)

    cache_factory = cache_factory or dict

    @wraps(method)
    def memoized_method_property(self):
        cache = cache_factory()
        cache_attr = "_%s_cache" %(method.__name__, )
        setattr(self, cache_attr, cache)
        result = partial(
            _memoized_call,
            partial(method, self),
            cache
        )
        result.memoize_cache = cache
        return result
    return memoized_property(memoized_method_property)


def deprecated(message, exception=PendingDeprecationWarning):
    """Throw a warning when a function/method will be soon deprecated

    Supports passing a ``message`` and an ``exception`` class
    (uses ``PendingDeprecationWarning`` by default). This is useful if you
    want to alternatively pass a ``DeprecationWarning`` exception for already
    deprecated functions/methods.

    Example::

        >>> import warnings
        >>> from functools import wraps
        >>> message = "this function will be deprecated in the near future"
        >>> @deprecated(message)
        ... def foo(n):
        ...     return n+n
        >>> with warnings.catch_warnings(record=True) as w:
        ...     warnings.simplefilter("always")
        ...     foo(4)
        ...     assert len(w) == 1
        ...     assert issubclass(w[-1].category, PendingDeprecationWarning)
        ...     assert message == str(w[-1].message)
        ...     assert foo.__name__ == 'foo'
        8
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, exception, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
