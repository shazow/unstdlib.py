import re
import string
import unicodedata

from .random_ import random


__all__ = [
    'random_string',
    'number_to_string', 'string_to_number', 'number_to_bytes', 'bytes_to_number',
    'dollars_to_cents',
    'to_str', 'to_unicode', 'to_int',
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


def bytes_to_number(b, endian='big'):
    """
    Convert a string to an integer.

    :param b:
        String or bytearray to convert.

    :param endian:
        Byte order to convert into ('big' or 'little' endian-ness, default
        'big')

    Assumes bytes are 8 bits.

    This is a special-case version of string_to_number with a full base-256
    ASCII alphabet. It is the reverse of ``number_to_bytes(n)``.

    Examples::

        >>> bytes_to_number('*')
        42
        >>> bytes_to_number('\\xff')
        255
        >>> bytes_to_number('\\x01\\x00')
        256
        >>> bytes_to_number('\\x00\\x01', endian='little')
        256
    """
    if endian == 'big':
        b = reversed(b)

    n = 0
    for i, ch in enumerate(bytearray(b)):
        n ^= ch << i * 8

    return n


def number_to_bytes(n, endian='big'):
    """
    Convert an integer to a corresponding string of bytes..

    :param n:
        Integer to convert.

    :param endian:
        Byte order to convert into ('big' or 'little' endian-ness, default
        'big')

    Assumes bytes are 8 bits.

    This is a special-case version of number_to_string with a full base-256
    ASCII alphabet. It is the reverse of ``bytes_to_number(b)``.

    Examples::

        >>> number_to_bytes(42)
        '*'
        >>> number_to_bytes(255)
        '\\xff'
        >>> number_to_bytes(256)
        '\\x01\\x00'
        >>> number_to_bytes(256, endian='little')
        '\\x00\\x01'
    """
    b = ''
    while n:
        n, ch = divmod(n, 256)
        b += chr(ch)

    if endian == 'big':
        return b[::-1]

    return b


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

    Examples::

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


def to_int(s, default=0):
    """
    Return input converted into an integer. If failed, then return ``default``.

    Examples::

        >>> to_int('1')
        1
        >>> to_int(1)
        1
        >>> to_int('')
        0
        >>> to_int(None)
        0
        >>> to_int(0, default='Empty')
        0
        >>> to_int(None, default='Empty')
        'Empty'
    """
    try:
        return int(s)
    except (TypeError, ValueError):
        return default


def dollars_to_cents(s, allow_negative=False):
    """
    Given a string or integer representing dollars, return an integer of
    equivalent cents, in an input-resilient way.

    Examples::

        >>> dollars_to_cents('$1')
        100
        >>> dollars_to_cents('1')
        100
        >>> dollars_to_cents(1)
        100
    """
    # TODO: Add support for "-$100"
    # TODO: Implement cents_to_dollars
    if not s:
        return

    if isinstance(s, basestring):
        s = s.lstrip('$')

    dollars = int(round(float(s) * 100))
    if not allow_negative and dollars < 0:
        raise ValueError('Negative values not permitted.')

    return dollars


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
