import sys

from unstdlib.six import reraise, PY3


__all__ = ['convert_exception']


def convert_exception(from_exception, to_exception, *to_args, **to_kw):
    """
    Decorator: Catch exception ``from_exception`` and instead raise ``to_exception(*to_args, **to_kw)``.

    Useful when modules you're using in a method throw their own errors that you want to
    convert to your own exceptions that you handle higher in the stack.

    Example: ::

        class FooError(Exception):
            pass

        class BarError(Exception):
            def __init__(self, message):
                self.message = message

        @convert_exception(FooError, BarError, message='bar')
        def throw_foo():
            raise FooError('foo')

        try:
            throw_foo()
        except BarError as e:
            assert e.message == 'bar'
    """
    def wrapper(fn):

        def fn_new(*args, **kw):
            try:
                return fn(*args, **kw)
            except from_exception:
                new_exception = to_exception(*to_args, **to_kw)
                traceback = sys.exc_info()[2]
                if PY3:
                    value = new_exception
                else:
                    value = None
                reraise(new_exception, value, traceback)

        fn_new.__doc__ = fn.__doc__
        return fn_new

    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
