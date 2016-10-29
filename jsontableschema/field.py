# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import re
import six
from copy import deepcopy
from functools import partial
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

    @property
    def required(self):
        """bool: true if field is required
        """
        return self.constraints.get('required', False)

    def cast_value(self, value, skip_constraints=False):
        """Cast value against field.

        Args:
            value (mixed): value to cast
            skip_constraints (bool): skip constraints if true

        Returns:
            mixed: cast value

        """
        return self.__type.cast(value, skip_constraints=skip_constraints)

    def test_value(self, value, skip_constraints=False, constraint=None):
        """Cast value against field.

        If no cast error unique constraint is alway passed.

        Args:
            value (mixed): value to test
            skip_constraints (bool): skip constraints if true
            constraint (str): constraint to test against (priority over skip)
                - required
                - pattern
                - unique
                - enum
                - minimum
                - maximum
                - minLenght
                - maxLength

        Returns:
            bool: test result

        """

        # General test
        if constraint is None:
            try:
                self.__type.cast(value, skip_constraints=skip_constraints)
            except (exceptions.InvalidCastError, exceptions.ConstraintError):
                return False

        # Granular test
        if constraint in self.__type.supported_constraints + ['unique']:
            if constraint not in ['required', 'pattern']:
                try:
                    value = self.__type.cast(value, skip_constraints=True)
                except exceptions.InvalidCastError:
                    return False
            validator = getattr(self, '_Field__validate_%s' % constraint)
            try:
                validator(value)
            except exceptions.ConstraintError:
                return False

        return True

    # Private

    # Family of validate methods could use cache
    # of constraint params to improve performance

    def __validate_required(self, value):
        """Validate value against required constraint.
        """
        if self.required and value in (self.__type.null_values + ['', None]):
            message = 'The field "%s" requires a value' % self.name
            raise exceptions.ConstraintError(message)
        return True

    def __validate_pattern(self, value):
        """Validate value against pattern constraint.
        """
        pattern = self.constraints.get('pattern')
        if pattern is not None and isinstance(value, six.string_types):
            regex = re.compile('^{0}$'.format(pattern))
            match = regex.match(value)
            if not match:
                message = 'The value for field "%s" must match the pattern"%s"'
                message = message % (self.name, pattern)
                raise exceptions.ConstraintError(message)
        return True

    def __validate_unique(self, value):
        """Validate CAST value against unique constraint.
        """
        return True

    def __validate_enum(self, value):
        """Validate CAST value against enum constraint.
        """
        enum = self.constraints.get('enum')
        if enum is not None:
            enum = map(partial(self.cast_value, skip_constraints=True), enum)
            if value not in enum:
                message = 'The value for field "%s" must be in enum "%s"'
                message = message % (self.name, enum)
                raise exceptions.ConstraintError(message)
        return True

    def __validate_minimum(self, value):
        """Validate CAST value against minimum constraint.
        """
        minimum = self.constraints.get('minimum')
        if minimum is not None:
            minimum = self.cast_value(minimum, skip_constraints=True)
            if value < minimum:
                message = 'The field "%s" must not be less than "%s"'
                message = message % (self.name, minimum)
                raise exceptions.ConstraintError(message)
        return True

    def __validate_maximum(self, value):
        """Validate CAST value against maximum constraint.
        """
        maximum = self.constraints.get('maximum')
        if maximum is not None:
            maximum = self.cast_value(maximum, skip_constraints=True)
            if value > maximum:
                message = 'The field "%s" must not be more than "%s"'
                message = message % (self.name, maximum)
                raise exceptions.ConstraintError(message)
        return True

    def __validate_minLength(self, value):
        """Validate CAST value against minLength constraint.
        """
        min_length = self.constraints.get('minLength')
        if min_length is not None:
            if len(value) < min_length:
                message = 'The field "%s" must have a minimum length of "%s"'
                message = message % (self.name, min_length)
                raise exceptions.ConstraintError(message)
        return True

    def __validate_maxLength(self, value):
        """Validate CAST value against maxLength constraint.
        """
        max_length = self.constraints.get('maxLength')
        if max_length is not None:
            if len(value) > max_length:
                message = 'The field "%s" must have a maximum length of "%s"'
                message = message % (self.name, max_length)
                raise exceptions.ConstraintError(message)
        return True


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
