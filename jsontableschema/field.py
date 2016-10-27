# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import deepcopy
from . import exceptions
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
        """dict: field descriptor
        """
        return self.__descriptor

    @property
    def name(self):
        """str: field name
        """
        return self.__descriptor['name']

    @property
    def type(self):
        """str: field type
        """
        return self.__descriptor.get('type', 'string')

    @property
    def format(self):
        """str: field format
        """
        return self.__descriptor.get('format', 'default')

    @property
    def constraints(self):
        """dict: field constraints
        """
        return self.__descriptor.get('constraints', {})

    def cast_value(self, value, skip_constraints=False):
        """Cast value against field.

        Args:
            value (mixed): value to cast
            skip_constraints (bool): skip constraints if true

        Return:
            mixed: cast value

        """
        return self.__type.cast(value, skip_constraints=skip_constraints)

    def test_value(self, value, skip_constraints=False, constraint=None):
        """Cast value against field.

        Args:
            value (mixed): value to test
            skip_constraints (bool): skip constraints if true
            constraint (str): constraint to test against
                - enum
                - maximum
                - maxLength
                - minimum
                - minLenght
                - pattern
                - required

        """

        # General approach
        if constraint is None:
            try:
                self.__type.cast(value, skip_constraints=skip_constraints)
                return True
            except (exceptions.InvalidCastError, exceptions.ConstraintError):
                return False

        # Granular constraint
        else:
            raise NotImplementedError()


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
