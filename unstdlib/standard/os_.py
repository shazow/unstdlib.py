import os

class chdir(object):
    """ A drop-in replacement for ``os.chdir`` which can also be used as a
    context manager.

    Example::

        >>> old_cwd = os.getcwd()
        >>> with chdir("/usr/"):
        ...     print("current dir: {0}".format(os.getcwd()))
        ...
        current dir: /usr
        >>> os.getcwd() == old_cwd
        True
        >>> x = chdir("/usr/")
        >>> os.getcwd()
        '/usr'
        >>> x.unchdir()
        >>> os.getcwd() == old_cwd
        True
    """

    def __init__(self, new_path, old_path=None):
        self.old_path = old_path or os.getcwd()
        self.new_path = new_path
        self.chdir()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.unchdir()

    def chdir(self):
        os.chdir(self.new_path)

    def unchdir(self):
        os.chdir(self.old_path)

    def __repr__(self):
        return "%s(%r, old_path=%r)" %(
            type(self).__name__, self.new_path, self.old_path,
        )

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
