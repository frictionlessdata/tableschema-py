# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import json


# Internal

def _load_spec(filename):
    path = os.path.join(os.path.dirname(__file__), 'specs', filename)
    spec = json.load(io.open(path, encoding='utf-8'))
    return spec


# Public API

table_schema = _load_spec('table-schema.json')
geojson = _load_spec('geojson.json')
