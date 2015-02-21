#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

from setuptools import setup

long_description = open('README.rst').read()

exec(open('bloscpack/version.py').read())

install_requires = [
    'blosc>=1.2.0',
    'numpy'
]

tests_require = [
    'nose',
    'cram>=0.6',
    'mock',
    'coverage',
]

setup(
    name = "bloscpack",
    version = __version__,
    packages = ['bloscpack'],
    entry_points = {
        'console_scripts' : [
            'blpk = bloscpack.cli:main',
        ]
    },
    author = "Valentin Haenel",
    author_email = "valentin@haenel.co",
    description = "Command line interface to and serialization format for Blosc",
    long_description=long_description,
    license = "MIT",
    keywords = ('compression', 'applied information theory'),
    url = "https://github.com/blosc/bloscpack",
    install_requires = install_requires,
    extras_require = dict(tests=tests_require),
    tests_require = tests_require,
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: System :: Archiving :: Compression',
                   'Topic :: Utilities',
                  ],
     )
