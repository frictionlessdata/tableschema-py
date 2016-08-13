# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import requests
from jsontableschema.schema import Schema


# Constants

FPATH = 'data/%s'
WPATH = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/data/%s'
DESCRIPTOR = {'fields': [{'name': 'id'}]}


# Tests

def test_descriptor():
    # Dict
    assert Schema(DESCRIPTOR).descriptor == DESCRIPTOR
    # Path
    path = FPATH % 'schema_valid_simple.json'
    expect = Schema(path).descriptor
    actual = json.load(io.open(path, encoding='utf-8'))
    assert expect == actual
    # Url
    url = WPATH % 'schema_valid_simple.json'
    expect = Schema(url).descriptor
    actual = requests.get(url).json()
    assert expect == actual
