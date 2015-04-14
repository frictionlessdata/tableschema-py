"""useful models for JSON Table Schema."""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json
from . import _types
from . import exceptions
from . import utilities
from .ensure import ensure


class SchemaModel(object):

    """Model for a JSON Table Schema.

    Providers handy helpers for ingesting, validating and outputting 
    JSON Table Schemas: http://dataprotocols.org/json-table-schema/

    Args:
        * schema_source (string or dict): A filepath, url or dictionary 
        that represents a schema
        * case_insensitive_headers (bool): if True, headers should be 
        considered case insensitive, and `SchemaModel` forces all 
        headers to lowercase when they are represented via a model 
        instance. This setting **does not** mutate the actual strings 
        that come from the the input schema_source, so out put methods
        such as as_python and as_json are **not** subject to this flag.

    """

    NULL_VALUES = [None] + utilities.NULL_VALUES
    TRUE_VALUES = [True] + utilities.TRUE_VALUES
    FALSE_VALUES = [False] + utilities.FALSE_VALUES

    DEFAULTS = {
        'constraints': {'required': True},
        'format': 'default',
        'type': 'string'
    }

    def __init__(self, schema_source, case_insensitive_headers=False):

        self.schema_source = schema_source
        self.case_insensitive_headers = case_insensitive_headers
        _as_python = self._to_python()

        if _as_python is None:
            raise exceptions.InvalidJSONError
        
        if not ensure(_as_python)[0]:
            raise exceptions.InvalidSchemaError

        self.as_python = self._expand(_as_python)
        self.as_json = json.dumps(self.as_python)

    @property
    def headers(self):
        _raw = [f['name'] for f in self.as_python.get('fields')]
        if self.case_insensitive_headers:
            return [name.lower() for name in _raw]
        return _raw

    @property
    def required_headers(self):
        _raw = [f['name'] for f in self.as_python.get('fields')
                if f['constraints']['required']]
        if self.case_insensitive_headers:
            return [name.lower() for name in _raw]
        return _raw

    @property
    def primaryKey(self):
        return self.as_python.get('primaryKey')

    @property
    def foreignKeys(self):
        return self.as_python.get('foreignKeys')

    @property
    def fields(self):
        return [f for f in self.as_python.get('fields')]

    def cast(self, field_name, value, index=0):
        """Return boolean if value can be cast to field_name's type."""

        _type = self.get_type(field_name, index=index)

        return _type.cast(value)

    def get_field(self, field_name, index=0):
        """Return the `field` object for `field_name`.

        `index` allows accessing a field name by position, as JTS allows
        duplicate field names.

        """

        try:
            return [f for f in self.fields if f['name'] == field_name][index]
        except IndexError:
            return None

    def has_field(self, field_name):
        """Return boolean if the field exists in the schema."""

        return bool(self.get_field(field_name))

    def get_type(self, field_name, index=0):
        """Return the `type` for `field_name`."""

        _field = self.get_field(field_name, index=index)
        _class = self._type_map()[_field['type']]

        return _class(_field)

    def get_fields_by_type(self, type_name):
        """Return all fields that match the given type."""

        return [f for f in self.fields if f['type'] == type_name]

    def get_constraints(self, field_name, index=0):
        """Return the `constraints` object for `field_name`."""

        return self.get_field(field_name, index=index).get('constraints')

    def _to_python(self):
        """Return schema as a Python data structure (dict)."""

        try:
            return utilities.load_json_source(self.schema_source)
        except Exception:
            return None

    def _expand(self, schema):
        """Expand the schema with additional default properties."""

        for field in schema.get('fields', {}):

            # ensure we have a default type if no type was declared
            if not field.get('type'):
                field['type'] = self.DEFAULTS['type']

            # ensure we have a default format if no format was declared
            if not field.get('format'):
                field['format'] = self.DEFAULTS['format']

            # ensure we have a minimum constraints declaration
            if not field.get('constraints'):
                field['constraints'] = self.DEFAULTS['constraints']

            elif field['constraints'].get('required') is None:
                field['constraints']['required'] = self.DEFAULTS['constraints']['required']

        return schema

    @staticmethod
    def _type_map():
        """Map a JSON Table Schema type to a JTSKit type class."""

        return {
            'string': _types.StringType,
            'number': _types.NumberType,
            'integer': _types.IntegerType,
            'boolean': _types.BooleanType,
            'null': _types.NullType,
            'array': _types.ArrayType,
            'object': _types.ObjectType,
            'date': _types.DateType,
            'time': _types.TimeType,
            'datetime': _types.DateTimeType,
            'geopoint': _types.GeoPointType,
            'geojson': _types.GeoJSONType,
            'any': _types.AnyType
        }
