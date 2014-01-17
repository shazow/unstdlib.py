import re
import string
import unicodedata

from unstdlib.six import text_type, PY3, string_types, binary_type, u
from unstdlib.six.moves import xrange

if PY3:
    text_type_magicmethod = "__str__"
else:
    text_type_magicmethod = "__unicode__"

from .random_ import random


__all__ = [
    'random_string',
    'number_to_string', 'string_to_number', 'number_to_bytes', 'bytes_to_number',
    'dollars_to_cents',
    'to_str', 'to_unicode', 'to_int', 'to_float',
    'format_int',
    'slugify',
]

class r(object):
    """
    A normalized repr for bytes/unicode between Python2 and Python3.
    """
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        if PY3:
            if isinstance(self.val, text_type):
                return 'u' + repr(self.val)
        else:
            if isinstance(self.val, str):
                return 'b' + repr(self.val)
        return repr(self.val)


_Default = object()

def random_string(length=6, alphabet=string.ascii_letters+string.digits):
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

        >>> number_to_string(12345678, string.ascii_letters + string.digits)
        'ZXP0'

        >>> number_to_string(12345, ['zero ', 'one ', 'two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 'eight ', 'nine '])
        'one two three four five '

    """
    result = ''
    base = len(alphabet)
    current = int(n)
    if current < 0:
        raise ValueError("invalid n (must be non-negative): %s", n)
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

        >>> string_to_number('ZXP0', string.ascii_letters + string.digits)
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

        >>> bytes_to_number(b'*')
        42
        >>> bytes_to_number(b'\\xff')
        255
        >>> bytes_to_number(b'\\x01\\x00')
        256
        >>> bytes_to_number(b'\\x00\\x01', endian='little')
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

        >>> r(number_to_bytes(42))
        b'*'
        >>> r(number_to_bytes(255))
        b'\\xff'
        >>> r(number_to_bytes(256))
        b'\\x01\\x00'
        >>> r(number_to_bytes(256, endian='little'))
        b'\\x00\\x01'
    """
    res = []
    while n:
        n, ch = divmod(n, 256)
        if PY3:
            res.append(ch)
        else:
            res.append(chr(ch))

    if endian == 'big':
        res.reverse()

    if PY3:
        return bytes(res)
    else:
        return ''.join(res)


def to_str(obj, encoding='utf-8', **encode_args):
    r"""
    Returns a ``str`` of ``obj``, encoding using ``encoding`` if necessary. For
    example::

        >>> some_str = b"\xff"
        >>> some_unicode = u"\u1234"
        >>> some_exception = Exception(u'Error: ' + some_unicode)
        >>> r(to_str(some_str))
        b'\xff'
        >>> r(to_str(some_unicode))
        b'\xe1\x88\xb4'
        >>> r(to_str(some_exception))
        b'Error: \xe1\x88\xb4'
        >>> r(to_str([42]))
        b'[42]'

    See source code for detailed semantics.
    """
    # Note: On py3, ``b'x'.__str__()`` returns ``"b'x'"``, so we need to do the
    # explicit check first.
    if isinstance(obj, binary_type):
        return obj

    # We coerce to unicode if '__unicode__' is available because there is no
    # way to specify encoding when calling ``str(obj)``, so, eg,
    # ``str(Exception(u'\u1234'))`` will explode.
    if isinstance(obj, text_type) or hasattr(obj, text_type_magicmethod):
        # Note: unicode(u'foo') is O(1) (by experimentation)
        return text_type(obj).encode(encoding, **encode_args)

    return binary_type(obj)


def to_unicode(obj, encoding='utf-8', fallback='latin1', **decode_args):
    r"""
    Returns a ``unicode`` of ``obj``, decoding using ``encoding`` if necessary.
    If decoding fails, the ``fallback`` encoding (default ``latin1``) is used.

    Examples::

        >>> r(to_unicode(b'\xe1\x88\xb4'))
        u'\u1234'
        >>> r(to_unicode(b'\xff'))
        u'\xff'
        >>> r(to_unicode(u'\u1234'))
        u'\u1234'
        >>> r(to_unicode(Exception(u'\u1234')))
        u'\u1234'
        >>> r(to_unicode([42]))
        u'[42]'

    See source code for detailed semantics.
    """

    # Note: on py3, the `bytes` type defines an unhelpful "__str__" function,
    # so we need to do this check (see comments in ``to_str``).
    if not isinstance(obj, binary_type):
        if isinstance(obj, text_type) or hasattr(obj, text_type_magicmethod):
            return text_type(obj)

        obj_str = binary_type(obj)
    else:
        obj_str = obj

    try:
        return text_type(obj_str, encoding, **decode_args)
    except UnicodeDecodeError:
        return text_type(obj_str, fallback, **decode_args)


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


_infs=set([float("inf"), float("-inf")])

def to_float(s, default=0.0, allow_nan=False):
    """
    Return input converted into a float. If failed, then return ``default``.

    Note that, by default, ``allow_nan=False``, so ``to_float`` will not return
    ``nan``, ``inf``, or ``-inf``.

    Examples::

        >>> to_float('1.5')
        1.5
        >>> to_float(1)
        1.0
        >>> to_float('')
        0.0
        >>> to_float('nan')
        0.0
        >>> to_float('inf')
        0.0
        >>> to_float('-inf', allow_nan=True)
        -inf
        >>> to_float(None)
        0.0
        >>> to_float(0, default='Empty')
        0.0
        >>> to_float(None, default='Empty')
        'Empty'
    """
    try:
        f = float(s)
    except (TypeError, ValueError):
        return default
    if not allow_nan:
        if f != f or f in _infs:
            return default
    return f


def format_int(n, singular=_Default, plural=_Default):
    """
    Return `singular.format(n)` if n is 1, or `plural.format(n)` otherwise. If
    plural is not specified, then it is assumed to be same as singular but
    suffixed with an 's'.

    :param n:
        Integer which determines pluralness.

    :param singular:
        String with a format() placeholder for n. (Default: `u"{:,}"`)

    :param plural:
        String with a format() placeholder for n. (Default: If singular is not
        default, then it's `singular + u"s"`. Otherwise it's same as singular.)

    Example: ::

        >>> r(format_int(1000))
        u'1,000'
        >>> r(format_int(1, u"{} day"))
        u'1 day'
        >>> r(format_int(2, u"{} day"))
        u'2 days'
        >>> r(format_int(2, u"{} box", u"{} boxen"))
        u'2 boxen'
        >>> r(format_int(20000, u"{:,} box", u"{:,} boxen"))
        u'20,000 boxen'
    """
    n = int(n)

    if singular in (None, _Default):
        if plural is _Default:
            plural = None

        singular = u'{:,}'

    elif plural is _Default:
        plural = singular + u's'

    if n == 1 or not plural:
        return singular.format(n)

    return plural.format(n)



RE_NUMBER = re.compile(r'[\d\.\-eE]+')

def dollars_to_cents(s, allow_negative=False):
    """
    Given a string or integer representing dollars, return an integer of
    equivalent cents, in an input-resilient way.
    
    This works by stripping any non-numeric characters before attempting to
    cast the value.

    Examples::

        >>> dollars_to_cents('$1')
        100
        >>> dollars_to_cents('1')
        100
        >>> dollars_to_cents(1)
        100
        >>> dollars_to_cents('1e2')
        10000
        >>> dollars_to_cents('-1$', allow_negative=True)
        -100
        >>> dollars_to_cents('1 dollar')
        100
    """
    # TODO: Implement cents_to_dollars
    if not s:
        return

    if isinstance(s, string_types):
        s = ''.join(RE_NUMBER.findall(s))

    dollars = int(round(float(s) * 100))
    if not allow_negative and dollars < 0:
        raise ValueError('Negative values not permitted.')

    return dollars


RE_SLUG = re.compile(r'\W+')

def slugify(s, delimiter='-'):
    """
    Normalize `s` into ASCII and replace non-word characters with `delimiter`.
    """
    s = unicodedata.normalize('NFKD', to_unicode(s)).encode('ascii', 'ignore').decode('ascii')
    return RE_SLUG.sub(delimiter, s).strip(delimiter).lower()


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
