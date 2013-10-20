__all__ = ['is_subclass']


_issubclass = issubclass

def is_subclass(o, bases):
    """
    Similar to the ``issubclass`` builtin, but does not raise a ``TypeError``
    if either ``o`` or ``bases`` is not an instance of ``type``.

    Example::

        >>> is_subclass(IOError, Exception)
        True
        >>> is_subclass(Exception, None)
        False
        >>> is_subclass(None, Exception)
        False
        >>> is_subclass(IOError, (None, Exception))
        True
        >>> is_subclass(Exception, (None, 42))
        False
    """
    try:
        return _issubclass(o, bases)
    except TypeError:
        pass

    if not isinstance(o, type):
        return False
    if not isinstance(bases, tuple):
        return False

    bases = tuple(b for b in bases if isinstance(b, type))
    return _issubclass(o, bases)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
