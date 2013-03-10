import os.path
import hashlib
import time

from functools_ import memoized_into
from list_ import iterate_dict


_IMPORT_TIME = str(int(time.time()))

_BUST_METHODS = {
    'mtime': lambda src_path: str(int(os.path.getmtime(src_path))),
    'md5': lambda src_path: hashlib.md5(open(src_path).read()).hexdigest(),
    'importtime': lambda src_path: _IMPORT_TIME,
}

_BUST_CACHE = {}


@memoized_into(_BUST_CACHE)
def get_cache_buster(src_path, method='importtime'):
    """ Return a string that can be used as a parameter for cache-busting URLs
    for this asset.

    NOTE: The returned value is cached, to avoid doing processing if it's
    called repeatedly with the same parameters.

    :param src_path:
        Filesystem path to the file we're generating a cache-busting value for.

    :param method:
        Method for cache-busting. Supported values: importtime, mtime, md5
        The default is 'importtime', because it requires the least processing.


    Example::

        >>> get_cache_buster('html.py') is _IMPORT_TIME
        True
        >>> get_cache_buster('html.py', method='mtime') is not _IMPORT_TIME  # FIXME: Is there a better doctest example?
        True
        >>> get_cache_buster('html.py', method='md5') is not _IMPORT_TIME  # FIXME: Is there a better doctest example?
        True
    """
    try:
        fn = _BUST_METHODS[method]
    except KeyError:
        raise KeyError('Unsupported busting method value: %s' % method)

    return fn(src_path)


def _generate_dom_attrs(attrs, allow_no_value=True):
    """ Yield compiled DOM attribute key-value strings.

    If the value is `False`, then it is treated as no-value."""
    for attr in iterate_dict(attrs):
        if isinstance(attr, basestring):
            attr = (attr, False)
        key, value = attr
        if value is False and not allow_no_value:
            value = key  # E.g. <option checked="checked" />
        if value is False:
            yield value  # E.g. <option checked />
        else:
            yield '%s="%s"' % (key, value.replace('"', '\\"'))


def html_tag(tagname, body='', attrs=None):
    """ Helper for programmatically building HTML tags.

    Note that this barely does any escaping, and will happily spit out
    dangerous user input if used as such.

    :param tagname:
        Tag name of the DOM element we want to return.

    :param body:
        Optional body of the DOM element. If `False`, then the element is
        self-closed.

    :param attrs:
        Optional dictionary-like collection of attributes for the DOM element.

    Example::

        >>> html_tag('div', body='Hello, world.')
        '<div>Hello, world.</div>'
        >>> html_tag('script', attrs={'src': '/static/js/core.js'})
        '<script src="/static/js/core.js"></script>'
        >>> html_tag('script', attrs=[('src', '/static/js/core.js'), ('type', 'text/javascript')])
        '<script src="/static/js/core.js" type="text/javascript"></script>'
        >>> html_tag('meta', body=False, attrs=dict(content='"quotedquotes"'))
        '<meta content="\\\\"quotedquotes\\\\"" />'
    """
    attrs_str = attrs and ' '.join(_generate_dom_attrs(attrs))
    open_tag = tagname
    if attrs_str:
        open_tag += ' ' + attrs_str
    if body is False:
        return '<%s />' % open_tag
    return '<%s>%s</%s>' % (open_tag, body, tagname)


def html_javascript_link(src_url, src_path=None, cache_bust=None, body='', extra_attrs=None):
    """ Helper for programmatically building HTML JavaScript source include
    links, with optional cache busting.

    :param src_url:
        Goes into the `src` attribute of the `<script src="...">` tag.

    :param src_path:
        Optional filesystem path to the source file, used when `cache_bust` is
        enabled.

    :param body:
        Optional body of the DOM element. If `False`, then the element is
        self-closed.

    :param cache_bust:
        Optional method to use for cache busting. Can be one of: importtime,
        md5, or mtime. If the value is md5 or mtime, then `src_path` must be
        supplied.


    Example::

        >>> html_javascript_link('/static/js/core.js')
        '<script src="/static/js/core.js" type="text/javascript"></script>'
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

    return html_tag('script', body=body, attrs=attrs)


def html_stylesheet_link(src_url, src_path=None, cache_bust=None, body='', extra_attrs=None):
    """ Helper for programmatically building HTML StyleSheet source include
    links, with optional cache busting.

    :param src_url:
        Goes into the `src` attribute of the `<link src="...">` tag.

    :param src_path:
        Optional filesystem path to the source file, used when `cache_bust` is
        enabled.

    :param body:
        Optional body of the DOM element. If `False`, then the element is
        self-closed.

    :param cache_bust:
        Optional method to use for cache busting. Can be one of: importtime,
        md5, or mtime. If the value is md5 or mtime, then `src_path` must be
        supplied.


    Example::

        >>> html_stylesheet_link('/static/css/media.css')
        '<link href="/static/css/media.css" rel="stylesheet"></link>'
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

    return html_tag('link', body=body, attrs=attrs)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
