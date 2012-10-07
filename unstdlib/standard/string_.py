import random
import re
import string
import unicodedata


__all__ = [
    'random_string',
    'number_to_string', 'string_to_number',
    'to_str', 'to_unicode',
    'slugify',
]


def random_string(length=6, alphabet=string.letters+string.digits):
    """
    Return a random string of given length and alphabet.

    Default alphabet is url-friendly (base62).
    """
    return ''.join([random.choice(alphabet) for i in xrange(length)])


def number_to_string(n, alphabet):
    """
    Given an non-negative integer ``n``, convert it to a string composed of
    the given ``alphabet`` mapping, where the position of each element in
    ``alphabet`` is its radix value.

    Examples::

        >>> number_to_string(12345678, '01')
        '101111000110000101001110'

        >>> number_to_string(12345678, 'ab')
        'babbbbaaabbaaaababaabbba'

        >>> number_to_string(12345678, string.letters + string.digits)
        'ZXP0'

        >>> number_to_string(12345, ['zero ', 'one ', 'two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 'eight ', 'nine '])
        'one two three four five '

    """
    result = ''
    base = len(alphabet)
    current = int(n)
    while current:
        result = alphabet[current % base] + result
        current = current // base

    return result


def string_to_number(s, alphabet):
    """
    Given a string ``s``, convert it to an integer composed of the given
    ``alphabet`` mapping, where the position of each element in ``alphabet`` is
    its radix value.

    Examples::

        >>> string_to_number('101111000110000101001110', '01')
        12345678

        >>> string_to_number('babbbbaaabbaaaababaabbba', 'ab')
        12345678

        >>> string_to_number('ZXP0', string.letters + string.digits)
        12345678

    """
    base = len(alphabet)
    inverse_alphabet = dict(zip(alphabet, xrange(0, base)))
    n = 0
    exp = 0
    for i in reversed(s):
        n += inverse_alphabet[i] * (base ** exp)
        exp += 1

    return n


def to_str(obj, encoding='utf-8', **encode_args):
    r"""
    Returns a ``str`` of ``obj``, encoding using ``encoding`` if necessary. For
    example::

        >>> some_str = "\xff"
        >>> some_unicode = u"\u1234"
        >>> some_exception = Exception(u'Error: ' + some_unicode)
        >>> to_str(some_str)
        '\xff'
        >>> to_str(some_unicode)
        '\xe1\x88\xb4'
        >>> to_str(some_exception)
        'Error: \xe1\x88\xb4'
        >>> to_str([u'\u1234', 42])
        "[u'\\u1234', 42]"

    See source code for detailed semantics.
    """
    # We coerce to unicode if '__unicode__' is available because there is no
    # way to specify encoding when calling ``str(obj)``, so, eg,
    # ``str(Exception(u'\u1234'))`` will explode.
    if isinstance(obj, unicode) or hasattr(obj, "__unicode__"):
        # Note: unicode(u'foo') is O(1) (by experimentation)
        return unicode(obj).encode(encoding, **encode_args)

    # Note: it's just as fast to do `if isinstance(obj, str): return obj` as it
    # is to simply return `str(obj)`.
    return str(obj)


def to_unicode(obj, encoding='utf-8', fallback='latin1', **decode_args):
    r"""
    Returns a ``unicode`` of ``obj``, decoding using ``encoding`` if necessary.
    If decoding fails, the ``fallback`` encoding (default ``latin1``) is used.

    For example::

        >>> to_unicode('\xe1\x88\xb4')
        u'\u1234'
        >>> to_unicode('\xff')
        u'\xff'
        >>> to_unicode(u'\u1234')
        u'\u1234'
        >>> to_unicode(Exception(u'\u1234'))
        u'\u1234'
        >>> to_unicode([u'\u1234', 42])
        u"[u'\\u1234', 42]"

    See source code for detailed semantics.
    """

    if isinstance(obj, unicode) or hasattr(obj, "__unicode__"):
        return unicode(obj)

    obj_str = str(obj)
    try:
        return unicode(obj_str, encoding, **decode_args)
    except UnicodeDecodeError:
        return unicode(obj_str, fallback, **decode_args)


RE_SLUG = re.compile(r'\W+')

def slugify(s, delimiter='-'):
    """
    Normalize `s` into ASCII and replace non-word characters with `delimiter`.
    """
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    return RE_SLUG.sub(delimiter, s).strip(delimiter).lower()


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
