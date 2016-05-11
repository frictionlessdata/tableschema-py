# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import jsonschema
from future.utils import raise_with_traceback
from .. import exceptions
from .. import utilities
from .. import compat
from . import base


# Module API

class GeoJSONType(base.JTSType):

    # Public

    name = 'geojson'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
    ]
    # ---
    python_type = dict
    spec = {
        'types': ['Point', 'MultiPoint', 'LineString', 'MultiLineString',
                  'Polygon', 'MultiPolygon', 'GeometryCollection', 'Feature',
                  'FeatureCollection']
    }

    def cast_default(self, value, fmt=None):
        if isinstance(value, self.python_type):
            try:
                jsonschema.validate(value, _geojson_schema)
                return value
            except jsonschema.exceptions.ValidationError as e:
                raise_with_traceback(exceptions.InvalidGeoJSONType())
        if isinstance(value, compat.str):
            try:
                geojson = json.loads(value)
                jsonschema.validate(geojson, _geojson_schema)
                return geojson
            except (TypeError, ValueError) as e:
                raise_with_traceback(exceptions.InvalidGeoJSONType())
            except jsonschema.exceptions.ValidationError as e:
                raise_with_traceback(exceptions.InvalidGeoJSONType())

    def cast_topojson(self, value, fmt=None):
        raise NotImplementedError


# Internal

def _load_geojson_schema():
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..', 'schemas', 'geojson.json')
    with open(filepath) as f:
        json_table_schema = json.load(f)
    return json_table_schema

_geojson_schema = _load_geojson_schema()
