__all__ = [
    'get_many', 'pop_many',
]


def get_many(d, required=[], optional=[], one_of=[]):
    """
    Returns a predictable number of elements out of ``d`` in a list for auto-expanding.

    Keys in ``required`` will raise KeyError if not found in ``d``.
    Keys in ``optional`` will return None if not found in ``d``.
    Keys in ``one_of`` will raise KeyError if none exist, otherwise return the first in ``d``.

    Example::

        uid, action, limit, offset = get_many(request.params, required=['uid', 'action'], optional=['limit', 'offset'])

    Note: This function has been added to the webhelpers package.
    """
    d = d or {}
    r = [d[k] for k in required]
    r += [d.get(k)for k in optional]

    if one_of:
        for k in (k for k in one_of if k in d):
            return r + [d[k]]

        raise KeyError("Missing a one_of value.")

    return r


def pop_many(d, keys, default=None):
    return [d.pop(k, default) for k in keys]


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
