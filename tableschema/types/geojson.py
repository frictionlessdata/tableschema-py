# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import six
import json
import jsonschema
from ..config import ERROR


# Module API

def cast_geojson(format, value):
    if not isinstance(value, dict):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = json.loads(value)
        except Exception:
            return ERROR
    if format == 'default':
        try:
            jsonschema.validate(value, _geojson_schema)
        except Exception:
            return ERROR
    elif format == 'topojson':
        if not isinstance(value, dict):
            return ERROR
    return value


# Internal

def _load_geojson_schema():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, '..', 'schemas', 'geojson.json')
    with open(filepath) as file:
        return json.load(file)

_geojson_schema = _load_geojson_schema()
