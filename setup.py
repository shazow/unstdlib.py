#!/usr/bin/env python

# ...

from distutils.core import setup
from web import __version__

setup(name='unstdlib.py',
    version=__version__,
    description='Unstandard Python library of useful and highly-reusable functions',
    author='Andrey Petrov',
    author_email='andrey.petrov@shazow.net',
    url='https://github.com/shazow/unstdlib.py',
    packages=['unstdlib'],
    long_description="""
    Have you ever written code that you used in more than one project? Me too.

    ``unstdlib`` is a compilation of highly-reusable code for Python.
    """.strip(),
    license="MIT",
    platforms=["any"],
)
