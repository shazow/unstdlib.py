import sys


def convert_exception(from_exception, to_exception, *to_args, **to_kw):
    """
    Decorator: Catch exception ``from_exception`` and instead raise ``to_exception(*to_args, **to_kw)``.

    Useful when modules you're using in a method throw their own errors that you want to
    convert to your own exceptions that you handle higher in the stack.

    Example:

    class FooError(Exception):
        pass

    class BarError(Exception):
        pass

    @convert_exception(FooError, BarError, message='bar')
    def throw_foo():
        raise FooError('foo')

    try:
        throw_foo()
    except BarError, e:
        assert e.message == 'bar'
    """
    def wrapper(fn):

        def fn_new(*args, **kw):
            try:
                return fn(*args, **kw)
            except from_exception, e:
                raise to_exception(*to_args, **to_kw), None, sys.exc_info()[2]

        fn_new.__doc__ = fn.__doc__
        return fn_new

    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
