# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import io
import json
from setuptools import setup, find_packages


_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)


DIR = os.path.abspath(os.path.dirname(__file__))
PKG = os.path.join(DIR, 'jsontableschema')
README = 'README.md'
LICENSE = 'LICENSE'
INFO = 'info.json'
README_PATH = os.path.join(DIR, README)
LICENSE_PATH = os.path.join(DIR, LICENSE)
INFO_PATH = os.path.join(PKG, INFO)

with io.open(README_PATH, mode='r+t', encoding='utf-8') as stream:
    description_text = stream.read()

with io.open(LICENSE_PATH, mode='r+t', encoding='utf-8') as stream:
    license_text = stream.read()

with io.open(INFO_PATH, mode='r+t', encoding='utf-8') as stream:
    info = json.loads(stream.read())

long_description = '{0}\n\n{1}'.format(description_text, license_text)

dependencies = [
    'click>=3.3',
    'requests>=2.5.1',
    'python-dateutil>=2.4.0',
    'rfc3987>=1.3.4',
    'jsonschema>=2.5.1',
    'future>=0.15.2'
]

classifiers = [
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
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(
    name=info['slug'],
    version=info['version'],
    description=info['description'],
    long_description=long_description,
    author=info['author'],
    author_email=info['author_email'],
    url=info['url'],
    license=info['license'],
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'jsontableschema': ['*.json', 'geojson/*json']},
    package_dir={info['slug']: info['slug']},
    install_requires=dependencies,
    zip_safe=False,
    keywords="open data frictionless data json schema json table schema data package tabular data package",
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'jsontableschema = jsontableschema.cli:main',
        ]
    }
)
