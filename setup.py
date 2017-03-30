# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
PACKAGE = 'tableschema'
NAME = PACKAGE.replace('_', '-')
INSTALL_REQUIRES = [
    'six>=1.9,<2.0a',
    'click>=3.3,<7.0a',
    'requests>=2.5,<3.0a',
    'python-dateutil>=2.4,<3.0a',
    'jsonschema>=2.5,<3.0a',
    'rfc3986>=0.4,<1.0a',
    'future>=0.15,<1.0a',
    'unicodecsv>=0.14,<1.0a',
    'tabulator>=0.7,<1.0a',
    'isodate>=0.5.4,<1.0a',
]
TESTS_REQUIRE = [
    'pylama',
    'tox',
]
README = read('README.md')
VERSION = read(PACKAGE, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'develop': TESTS_REQUIRE},
    entry_points={
        'console_scripts': [
            'tableschema = tableschema.cli:main',
        ]
    },
    zip_safe=False,
    long_description=README,
    description='A utility library for working with Table Schema in Python',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='https://github.com/frictionlessdata/tableschema-py',
    license='MIT',
    keywords=[
        'frictionless data',
        'open data',
        'json schema',
        'table schema',
        'data package',
        'tabular data package',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
