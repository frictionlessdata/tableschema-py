# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import deepcopy
from . import types


# Module API

class Field(object):
    """JSON Table Schema field representation.
    """

    # Public

    def __init__(self, descriptor):
        self.__descriptor = deepcopy(descriptor)
        # Probably it's just a temporal solution
        self.__type = _TYPES[self.type](descriptor)

    @property
    def descriptor(self):
        return self.__descriptor

    @property
    def name(self):
        return self.__descriptor['name']

    @property
    def type(self):
        return self.__descriptor.get('type', 'string')

    @property
    def format(self):
        return self.__descriptor.get('format', 'default')

    @property
    def constraints(self):
        return self.__descriptor.get('constraints', {})

    def cast_value(self, value):
        return self.__type.cast(value)


# Internal

_TYPES = {
    'string': types.StringType,
    'number': types.NumberType,
    'integer': types.IntegerType,
    'boolean': types.BooleanType,
    'null': types.NullType,
    'array': types.ArrayType,
    'object': types.ObjectType,
    'date': types.DateType,
    'time': types.TimeType,
    'datetime': types.DateTimeType,
    'geopoint': types.GeoPointType,
    'geojson': types.GeoJSONType,
    'any': types.AnyType,
}
