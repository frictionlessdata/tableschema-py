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
PACKAGE = 'jsontableschema'
NAME = PACKAGE.replace('_', '-')
INSTALL_REQUIRES = [
    'click>=3.3',
    'requests>=2.5.1',
    'python-dateutil>=2.4.0',
    'rfc3986>=0.3.0',
    'jsonschema>=2.5.1',
    'future>=0.15.2',
    'tabulator>=0.3',
    'unicodecsv>=0.14',
]
LINT_REQUIRES = [
    'pylint',
]
TESTS_REQUIRE = [
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
    extras_require={'develop': LINT_REQUIRES + TESTS_REQUIRE},
    entry_points={
        'console_scripts': [
            'jsontableschema = jsontableschema.cli:main',
        ]
    },
    zip_safe=False,
    long_description=README,
    description='A utility library for working with JSON Table Schema in Python',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='https://github.com/frictionlessdata/jsontableschema-py',
    license='MIT',
    keywords=[
        'frictionless data',
        'open data',
        'json schema',
        'json table schema',
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
