# Unstandard Library for Python

Have you ever written code that you used in more than one project? Me too.

This is a compilation of highly-reusable code for Python.

### Getting started

Install the latest release of unstdlib:

    $ pip install unstdlib

Use it in your code:

    from unstdlib import get_many, groupby_dict

    # ...

    user_id, sort_by, page_num = get_many(request.params, ['user_id'], optional=['sort_by', 'page_num'])

    # ...
    data_by_tags = groupby_dict(data, keyfunc=lambda o: o.tag)

    for n in data_by_tags['news']:
        print n


## Highlights

*(TODO: Format this better and select the most useful ones.)*

### [unstdlib.standard](https://github.com/shazow/unstdlib.py/blob/master/unstdlib/standard/)

* ``datetime_.iterate_date(start, stop=None, step=datetime.timedelta(days=1))``
* ``datetime_.iterate_date_values(d, start_date=None, stop_date=None, default=0)``
* ``datetime_.isoformat_as_datetime(s)``
* ``datetime_.truncate_datetime(t, resolution)``
* ``datetime_.now(timezone=None)``
* ``dict_.get_many(d, required=[], optional=[], one_of=[])``
* ``dict_.pop_many(d, keys, default=None)``
* ``@exception_.convert_exception(from_exception, to_exception, *to_args, **to_kw)``
* ``functools_.assert_hashable(*args, **kw)``
* ``@functools_.memoized(fn=None, cache=None)``
* ``@functools_.memoized_property(object)``
* ``@functools_.deprecated(message, exception=PendingDeprecationWarning)``
* ``list_.groupby_count(i, key=None, force_keys=None)``
* ``list_.iterate(maybe_iter, unless=(basestring, dict))``
* ``list_.is_iterable(maybe_iter, unless=(basestring, dict))``
* ``list_.iterate_chunks(i, size=10)``
* ``list_.iterate_items(dictish)``
* ``list_.iterate_flatten(q)``
* ``@list_.listify(fn=None, wrapper=list)``
* ``string_.random_string(length=6, alphabet=string.letters+string.digits)``
* ``string_.number_to_string(n, alphabet)``
* ``string_.string_to_number(s, alphabet)``
* ``string_.dollars_to_cents(s, allow_negative=False)``
* ``string_.to_str(obj, encoding='utf-8', **encode_args)``
* ``string_.to_unicode(obj, encoding='utf-8', fallback='latin1', **decode_args)``
* ``string_.to_int(s, default=0)``
* ``string_.format_int(n, singular=_Default, plural=_Default)``
* ``string_.slugify(s, delimiter='-')``
* ``type_.is_subclass(o, bases)``
* ``os_.chdir(new_dir)``: like ``os.chdir``, but also a context manager: ``with chdir("/tmp/"): pass``

### [unstdlib.formencode](https://github.com/shazow/unstdlib.py/blob/master/unstdlib/formencode.py)

* ``validate(d, key, validator)``
* ``validate_many(d, schema)``

### [unstdlib.sqlalchemy](https://github.com/shazow/unstdlib.py/blob/master/unstdlib/sqlalchemy.py)

* ``enumerate_query_by_limit(q, limit=1000)``

### [unstdlib.html](https://github.com/shazow/unstdlib.py/blob/master/unstdlib/html.py)

* ``get_cache_buster(src_path, method='importtime')``
* ``literal(s)``
* ``tag(tagname, content='', attrs=None)``
* ``javascript_link(src_url, src_path=None, cache_bust=None, content='', extra_attrs=None)``
* ``stylesheet_link(src_url, src_path=None, cache_bust=None, content='', extra_attrs=None)``


## Organization & Philosophy

This library includes code with no dependencies and code with dependencies.
Only the no-dependency code will be imported by default. Each collection of
code with a specific dependency is bundled under its own module (such as
Django-specific code).

* ``unstdlib.standard`` contains code that does not require additional
dependencies on top of Python 2.5.
* ``unstdlib.sqlalchemy`` contains code that is SQLAlchemy-specific.
* ``unstdlib.django`` (someday) contains code that is Django-specific.

We value simplicity and elegance over robustness and optimization. This library
should serve as a good foundation for your own application-specific code
instead of a complete framework. In other words, it is preferred to have a
2-line function that covers 80% of use cases than a 20-line function that
covers 100% of the use cases. Unexpected behaviour on bad input is fine as
long as expected usage is well documented.


## Contributors

Forks are highly encouraged. Everyone should have a collection of code they
commonly reuse. If you feel your code will be useful to others, make sure that
it is conforming to the spirit of the library outlined in the *Organization &
Philosophy* section and send over a pull request.

* [Full list of contributors](https://github.com/shazow/unstdlib.py/contributors)


## License

MIT (See LICENSE file).
