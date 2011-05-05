# Unstandard Library for Python

Have you ever written code that you used in more than one project? Me too.

This is a compilation of highly-reusable code for Python.


## Organization & Philosophy

This library includes code with no dependencies and code with dependencies.
Only the no-dependency code will be imported by default. Each collection of
code with a specific dependency is bundled under its own module (such as
Django-specific code).

* ``unstdlib.standard`` contains code that does not require additional
dependencies on top of Python 2.5.
* ``unstdlib.sqlalchemy`` (someday) contains code that is SQLAlchemy-specific.
* ``unstdlib.django`` (someday) contains code that is Django-specific.

We value simplicity and elegance over robustness and optimization. This library
should serve as a good foundation for your own application-specific code
instead of a complete framework. In other words, it is preferred to have a
2-line function that covers 80% of use cases than a 20-line function that
covers 100% of the use cases. Unexpected behaviour on bad input is fine as
long as expected usage is well documented.


## Highlights

*(TODO: Format this better and select the most useful ones.)*

* ``random_string(length=6, alphabet=string.letters+string.digits)``
* ``get_many(d, required=[], optional=[], one_of=[])``
* ``pop_many(d, keys, default=None)``
* ``groupby_count(i, key=None, force_keys=None)``
* ``groupby_dict(i, keyfunc=None)``
* ``iterate_date(start, stop=None, step=datetime.timedelta(days=1))``
* ``iterate_chunks(i, size=10)``
* ``iterate_flatten(q)``
* ``iterate_date_values(d, start_date=None, stop_date=None, default=0)``
* ``convert_exception(from_exception, to_exception, *to_args, **to_kw)``
* ``number_to_string(n, alphabet)``
* ``string_to_number(s, alphabet)``
* ``isoformat_as_datetime(s)``
* ``truncate_datetime(t, resolution)``
* ``validate(d, key, validator)``
* ``validate_many(d, schema)``

[Browse the unstdlib.standard code here](https://github.com/shazow/unstdlib.py/blob/master/unstdlib/standard/util.py).


## Contributors

Forks are highly encouraged. Everyone should have a collection of code they
commonly reuse. If you feel your code will be useful to others, make sure that
it is conforming to the spirit of the library outlined in the *Organization &
Philosophy* section and send over a pull request.

* [Full list of contributors](https://github.com/shazow/unstdlib.py/contributors)


## License

(The MIT License)

    Copyright 2011 Andrey Petrov <andrey.petrov@shazow.net>

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the 'Software'), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
