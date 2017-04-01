# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import jsonschema
from future.utils import raise_with_traceback
from ... import exceptions
from ... import helpers
from ... import compat
from ... import specs
from . import base


# Module API

class GeoJSONType(base.JTSType):

    # Public

    name = 'geojson'
    null_values = helpers.NULL_VALUES
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
                jsonschema.validate(value, specs.geojson)
                return value
            except jsonschema.exceptions.ValidationError:
                raise_with_traceback(exceptions.InvalidGeoJSONType())
        if isinstance(value, compat.str):
            try:
                geojson = json.loads(value)
                jsonschema.validate(geojson, specs.geojson)
                return geojson
            except (TypeError, ValueError):
                raise_with_traceback(exceptions.InvalidGeoJSONType())
            except jsonschema.exceptions.ValidationError:
                raise_with_traceback(exceptions.InvalidGeoJSONType())

    def cast_topojson(self, value, fmt=None):
        raise NotImplementedError
