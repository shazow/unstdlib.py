import os.path
import hashlib
import time

from unstdlib.standard.functools_ import memoized
from unstdlib.standard.list_ import iterate_items

try:
    import markupsafe
    MarkupType = markupsafe.Markup
except ImportError:
    MarkupType = unicode



__all__ = [
    'get_cache_buster', 'literal', 'tag', 'javascript_link', 'stylesheet_link',
]


@memoized
def _cache_key_by_md5(src_path, chunk_size=65536):
    hash = hashlib.md5()
    with open(src_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), ''):
            hash.update(chunk)
    return hash.hexdigest()


@memoized
def _cache_key_by_mtime(src_path):
    return str(int(os.path.getmtime(src_path)))


_IMPORT_TIME = str(int(time.time()))

_BUST_METHODS = {
    'mtime': _cache_key_by_mtime,
    'md5': _cache_key_by_md5,
    'importtime': lambda src_path: _IMPORT_TIME,
}


def get_cache_buster(src_path, method='importtime'):
    """ Return a string that can be used as a parameter for cache-busting URLs
    for this asset.

    :param src_path:
        Filesystem path to the file we're generating a cache-busting value for.

    :param method:
        Method for cache-busting. Supported values: importtime, mtime, md5
        The default is 'importtime', because it requires the least processing.

    Note that the mtime and md5 cache busting methods' results are cached on
    the src_path.

    Example::

        >>> SRC_PATH = os.path.join(os.path.dirname(__file__), 'html.py')
        >>> get_cache_buster(SRC_PATH) is _IMPORT_TIME
        True
        >>> get_cache_buster(SRC_PATH, method='mtime') == _cache_key_by_mtime(SRC_PATH)
        True
        >>> get_cache_buster(SRC_PATH, method='md5') == _cache_key_by_md5(SRC_PATH)
        True
    """
    try:
        fn = _BUST_METHODS[method]
    except KeyError:
        raise KeyError('Unsupported busting method value: %s' % method)

    return fn(src_path)


def _generate_dom_attrs(attrs, allow_no_value=True):
    """ Yield compiled DOM attribute key-value strings.

    If the value is `True`, then it is treated as no-value."""
    for attr in iterate_items(attrs):
        if isinstance(attr, basestring):
            attr = (attr, True)
        key, value = attr
        if value is True and not allow_no_value:
            value = key  # E.g. <option checked="true" />
        if value is True:
            yield True  # E.g. <option checked />
        else:
            yield '%s="%s"' % (key, value.replace('"', '\\"'))


class literal(MarkupType):
    """ Wrapper type which represents an HTML literal that does not need to be
    escaped. Will use `MarkupSafe` if available, otherwise it's a dumb
    unicode-like object.
    """
    def __html__(self):
        return self


def tag(tagname, content='', attrs=None):
    """ Helper for programmatically building HTML tags.

    Note that this barely does any escaping, and will happily spit out
    dangerous user input if used as such.

    :param tagname:
        Tag name of the DOM element we want to return.

    :param content:
        Optional content of the DOM element. If `None`, then the element is
        self-closed. By default, the content is an empty string.

    :param attrs:
        Optional dictionary-like collection of attributes for the DOM element.

    Example::

        >>> tag('div', content='Hello, world.')
        u'<div>Hello, world.</div>'
        >>> tag('script', attrs={'src': '/static/js/core.js'})
        u'<script src="/static/js/core.js"></script>'
        >>> tag('script', attrs=[('src', '/static/js/core.js'), ('type', 'text/javascript')])
        u'<script src="/static/js/core.js" type="text/javascript"></script>'
        >>> tag('meta', content=None, attrs=dict(content='"quotedquotes"'))
        u'<meta content="\\\\"quotedquotes\\\\"" />'
    """
    attrs_str = attrs and ' '.join(_generate_dom_attrs(attrs))
    open_tag = tagname
    if attrs_str:
        open_tag += ' ' + attrs_str
    if content or isinstance(content, basestring):
        return literal('<%s>%s</%s>' % (open_tag, content, tagname))
    return literal('<%s />' % open_tag)


def javascript_link(src_url, src_path=None, cache_bust=None, content='', extra_attrs=None):
    """ Helper for programmatically building HTML JavaScript source include
    links, with optional cache busting.

    :param src_url:
        Goes into the `src` attribute of the `<script src="...">` tag.

    :param src_path:
        Optional filesystem path to the source file, used when `cache_bust` is
        enabled.

    :param content:
        Optional content of the DOM element. If `None`, then the element is
        self-closed.

    :param cache_bust:
        Optional method to use for cache busting. Can be one of: importtime,
        md5, or mtime. If the value is md5 or mtime, then `src_path` must be
        supplied.


    Example::

        >>> javascript_link('/static/js/core.js')
        u'<script src="/static/js/core.js" type="text/javascript"></script>'
    """
    if cache_bust:
        append_suffix = get_cache_buster(src_path=src_path, method=cache_bust)
        delim = '&' if '?' in src_url else '?'
        src_url += delim + append_suffix

    attrs = {
        'src': src_url,
        'type': 'text/javascript',
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    return tag('script', content=content, attrs=attrs)


def stylesheet_link(src_url, src_path=None, cache_bust=None, content='', extra_attrs=None):
    """ Helper for programmatically building HTML StyleSheet source include
    links, with optional cache busting.

    :param src_url:
        Goes into the `src` attribute of the `<link src="...">` tag.

    :param src_path:
        Optional filesystem path to the source file, used when `cache_bust` is
        enabled.

    :param content:
        Optional content of the DOM element. If `None`, then the element is
        self-closed.

    :param cache_bust:
        Optional method to use for cache busting. Can be one of: importtime,
        md5, or mtime. If the value is md5 or mtime, then `src_path` must be
        supplied.


    Example::

        >>> stylesheet_link('/static/css/media.css')
        u'<link href="/static/css/media.css" rel="stylesheet"></link>'
    """
    if cache_bust:
        append_suffix = get_cache_buster(src_path=src_path, method=cache_bust)
        delim = '&' if '?' in src_url else '?'
        src_url += delim + append_suffix

    attrs = {
        'href': src_url,
        'rel': 'stylesheet',
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    return tag('link', content=content, attrs=attrs)


### Backwards compatibility (will be removed in v1.6):
__all__ += ['html_tag', 'html_javascript_link', 'html_stylesheet_link']

import warnings

def html_tag(*args, **kw):
    '''
    This function has been renamed to `tag`. Use that instead.
    Backwards-compatibility will be removed in v1.6.
    '''
    warnings.warn("Renamed to `tag`", DeprecationWarning)
    return tag(*args, **kw)


def html_javascript_link(*args, **kw):
    '''
    This function has been renamed to `javascript_link`. Use that instead.
    Backwards-compatibility will be removed in v1.6.
    '''
    warnings.warn("Renamed to `javascript_link`", DeprecationWarning)
    return javascript_link(*args, **kw)


def html_stylesheet_link(*args, **kw):
    '''
    This function has been renamed to `stylesheet_link`. Use that instead.
    Backwards-compatibility will be removed in v1.6.
    '''
    warnings.warn("Renamed to `stylesheet_link`", DeprecationWarning)
    return stylesheet_link(*args, **kw)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
