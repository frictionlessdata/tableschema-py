"""useful models for JSON Table Schema."""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json
from . import types
from . import exceptions
from . import utilities
from .validate import validate


class JSONTableSchema(object):

    def __init__(self, schema_source):

        self.schema_source = schema_source
        self.as_python = self._to_python()

        if not validate(self.as_python):
            raise exceptions.InvalidSchemaError

        self.as_json = json.dumps(self.as_python)

    @property
    def headers(self):
        return [f['name'] for f in self.as_python.get('fields')]

    @property
    def primaryKey(self):
        return self.as_python.get('primaryKey')

    @property
    def foreignKeys(self):
        return self.as_python.get('foreignKeys')

    @property
    def fields(self):
        return [f for f in self.as_python.get('fields')]

    def _to_python(self):
        """Return schema as a Python data structure (dict)."""
        as_python = utilities.load_json_source(self.schema_source)
        return as_python

    def _type_map(self):
        return {
            'string': types.StringType(),
            'number': types.NumberType(),
            'integer': types.IntegerType(),
            'date': types.DateType(),
            'time': types.TimeType(),
            'datetime': types.DateTimeType(),
            'boolean': types.BooleanType(),
            'binary': types.StringType(),
            'array': types.ArrayType(),
            'object': types.ObjectType(),
            'geopoint': (types.StringType(), types.ArrayType(), types.ObjectType()),
            'geojson': types.ObjectType(),
            'any': types.AnyType()
        }

    def get_field(self, field_name):
        """Return the `field` object for `field_name`."""
        return [f for f in self.fields if f['name'] == field_name][0]

    def get_type(self, field_name):
        """Return the `type` for `field_name`."""
        return self._type_map()[self.get_field(field_name).get('type', 'string')]

    def get_constraints(self, field_name):
        """Return the `constraints` object for `field_name`."""
        return self.get_field(field_name).get('constraints')

    def cast(self, field_name, value):
        """Return boolean if value can be cast to field_name's type."""

        _type = self.get_type(field_name)

        if isinstance(_type, collections.Iterable):
            return any([t.cast(value) for t in _type])

        return _type.cast(value)
