# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import pytest
import requests


def test_schemas_table_schema_is_up_to_date():
    actual = json.load(io.open('tableschema/schemas/table-schema.json', encoding='utf-8'))
    expect = requests.get('https://specs.frictionlessdata.io/schemas/table-schema.json').json()
    assert actual == expect, 'run `make schemas` to update schemas'
