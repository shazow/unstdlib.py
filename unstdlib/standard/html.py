import os.path
import hashlib
import time


_IMPORT_TIME = str(int(time.time()))


_BUST_METHODS = {
    'mtime': lambda src_path: str(int(os.path.getmtime(src_path))),
    'md5': lambda src_path: hashlib.md5(open(src_path).read()).hexdigest(),
    'importtime': lambda src_path: _IMPORT_TIME,
}


# TODO: Cache this.
def get_cache_buster(src_path, method='importtime'):
    """
    Return a string that can be used as a parameter for cache-busting URLs for
    this asset.

    NOTE: The returned value is cached, to avoid doing processing if it's
    called repeatedly with the same parameters.

    :param src_path:
        Filesystem path to the file we're generating a cache-busting value for.

    :param method:
        Method for cache-busting. Supported values: importtime, mtime, md5
        The default is 'importtime', because it requires the least processing.


    Example::

        >>> get_cache_buster('html.py')
        >>> get_cache_buster('html.py', method='mtime')
        >>> get_cache_buster('html.py', method='md5')
    """
    try:
        fn = _BUST_METHODS[method]
    except KeyError:
        raise KeyError('Unsupported busting method value: %s' % method)

    return fn(src_path)

