def validate(d, key, validator):
    """
    Validate a single value in ``d`` using a formencode validator.

    Example::

        email = validate(request.params, 'email', validators.Email(not_empty=True))
    """
    return validator.to_python(d.get(key))


def validate_many(d, schema):
    """Validate a dictionary of data against the provided schema.

    Returns a list of values positioned in the same order as given in ``schema``, each
    value is validated with the corresponding validator. Raises formencode.Invalid if
    validation failed.

    Similar to get_many but using formencode validation.

    :param d: A dictionary of data to read values from.
    :param schema: A list of (key, validator) tuples. The key will be used to fetch
        a value from ``d`` and the validator will be applied to it.

    Example::

        from formencode import validators

        email, password, password_confirm = validate_many(request.params, [
            ('email', validators.Email(not_empty=True)),
            ('password', validators.String(min=4)),
            ('password_confirm', validators.String(min=4)),
        ])
    """
    return [validator.to_python(d.get(key), state=key) for key,validator in schema]
