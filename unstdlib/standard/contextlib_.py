import os

def _doctest_setup():
    try:
        os.remove("/tmp/open_atomic-example.txt")
    except OSError:
        pass

class open_atomic(object):
    """
    Opens a file for atomic writing by writing to a temporary file, then moving
    the temporary file into place once writing has finished.

    When ``close()`` is called, the temporary file is moved into place,
    overwriting any file which may already exist (except on Windows, see note
    below). If moving the temporary file fails, ``abort()`` will be called *and
    an exception will be raised*.

    If ``abort()`` is called, the temporary file will be removed and the
    ``aborted`` attribute will be set to ``True``. No exception will be raised
    if an error is encountered while removing the temporary file; instead, the
    ``abort_error`` attribute will be set to the exception raised by
    ``os.remove`` (note: on Windows, if ``file.close()`` raises an exception,
    ``abort_error`` will be set to that exception; see implementation of
    ``abort()`` for details).

    By default, ``open_atomic`` will put the temporary file in the same
    directory as the target file:
    ``${dirname(target_file)}/.${basename(target_file)}.temp``. See also the
    ``prefix``, ``suffix``, and ``dir`` arguments to ``open_atomic()``. When
    changing these options, though, remember:

        * Moving files across filesystems is slow, so the temporary file should
          be stored on the same filesystem as the target file.
        * Using a random temporary name is likely a poor idea, as it's more
          likely that temporary files will be left lying around if a process is
          killed and re-started.
        * The temporary file will be blindly overwritten.

    .. note::
    
        ``open_atomic`` will appear to work on Windows, but will fail when the
        destination file exists, since ``os.rename`` will not overwrite the
        destination file (specifically, the call to ``close()`` will result in
        an exception being raised, and ``abort()`` being called).

    Example::

        >>> _doctest_setup()
        >>> f = open_atomic("/tmp/open_atomic-example.txt")
        >>> f.temp_name
        '/tmp/.open_atomic-example.txt.temp'
        >>> f.write("Hello, world!")
        >>> (os.path.exists(f.name), os.path.exists(f.temp_name))
        (False, True)
        >>> f.close()
        >>> os.path.exists("/tmp/open_atomic-example.txt")
        True

    By default, ``open_atomic`` uses the ``open`` builtin, but this behaviour
    can be changed using the ``open_func`` argument::

        >>> import io
        >>> f = open_atomic("/tmp/open_atomic-example.txt",
        ...                open_func=io.open,
        ...                mode="w+",
        ...                encoding="utf-8")
        >>> f.write(u"\u1234")
        1L
        >>> f.seek(0)
        0
        >>> f.read()
        u'\u1234'
        >>> f.close()

    """

    def __init__(self, name, prefix=".", suffix=".temp", dir=None, mode="w",
                 open_func=open, **open_args):
        self.name = name
        self.temp_name = self._get_temp_name(name, prefix, suffix, dir)
        self.fd = open_func(self.temp_name, mode, **open_args)
        self.closed = False
        self.aborted = False
        self.abort_error = None

    def _get_temp_name(self, target, prefix, suffix, dir):
        if dir is None:
            dir = os.path.dirname(target)
        return os.path.join(dir, "%s%s%s" %(
            prefix, os.path.basename(target), suffix,
        ))

    def close(self):
        if self.closed:
            return
        try:
            self.fd.close()
            os.rename(self.temp_name, self.name)
        except:
            try:
                self.abort()
            except:
                pass
            raise
        self.closed = True

    def abort(self):
        try:
            if os.name == "nt":
                # Note: Windows can't remove an open file, so sacrifice some
                # safety and close it before deleting it here. This is only a
                # problem if ``.close()`` raises an exception, which it really
                # shouldn't... But it's probably a better idea to be safe.
                self.fd.close()
            os.remove(self.temp_name)
        except OSError as e:
            self.abort_error = e
        self.fd.close()
        self.closed = True
        self.aborted = True

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        if exc_info[0] is None:
            self.close()
        else:
            self.abort()

    def __getattr__(self, attr):
        return getattr(self.fd, attr)
