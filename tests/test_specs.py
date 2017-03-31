# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import pytest
import requests
from tableschema import specs


def test_specs_table_schema_is_up_to_date():
    origin_spec = requests.get('https://specs.frictionlessdata.io/schemas/table-schema.json').json()
    assert specs.table_schema == origin_spec, 'run `make specs` to update specs'
