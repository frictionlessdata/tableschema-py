# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import deepcopy
from functools import partial
from . import constraints
from . import exceptions
from . import config
from . import specs
from . import types


# Module API

class Field(object):
    """Table Schema field representation.
    """

    # Public

    def __init__(self, descriptor, missing_values=config.DEFAULT_MISSING_VALUES):

        # Deepcopy descriptor
        descriptor = deepcopy(descriptor)

        # Apply descriptor defaults
        descriptor.setdefault('type', config.DEFAULT_FIELD_TYPE)
        descriptor.setdefault('format', config.DEFAULT_FIELD_FORMAT)

        # Set attributes
        self.__descriptor = descriptor
        self.__missing_values = missing_values
        self.__cast_function = self.__get_cast_function()
        self.__check_functions = self.__get_check_functions()

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
        return self.__descriptor['type']

    @property
    def format(self):
        """str: field format
        """
        return self.__descriptor['format']

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

    def cast_value(self, value, constraints=True):
        """Cast value against field.

        Args:
            value (any): value to cast
            constraints (None/str[]/False):
                - pass True to check all constraints (default)
                - pass list of constraints for granular check
                - pass False to skip all constraints

        Returns:
            any: cast value

        """

        # Null value
        if value in self.__missing_values:
            value = None

        # Cast value
        cast_value = value
        if value is not None:
            cast_value = self.__cast_function(value)
            if cast_value == config.ERROR:
                raise exceptions.InvalidCastError((
                    'Field "{field.name}" can\'t cast value "{value}" '
                    'for type "{field.type}" with format "{field.format}"'
                    ).format(field=self, value=value))

        # Check value
        if constraints:
            for name, check in self.__check_functions.items():
                if isinstance(constraints, list):
                    if name not in constraints:
                        continue
                passed = check(cast_value)
                if not passed:
                    raise exceptions.ConstraintError((
                        'Field "{field.name}" has constraint "{name}" '
                        'which is not satisfied for value "{value}"'
                        ).format(field=self, name=name, value=value))

        return cast_value

    def test_value(self, value, constraints=True):
        """Cast value against field.

        Args:
            value (mixed): value to test
            constraints (None/str[]/False):
                - pass True to check all constraints (default)
                - pass list of constraints for granular check
                - pass False to skip all constraints

        Returns:
            bool: result of test

        """
        try:
            self.cast_value(value, constraints=constraints)
        except (exceptions.InvalidCastError, exceptions.ConstraintError):
            return False
        return True

    # Private

    def __get_cast_function(self):
        options = {}
        # Get cast options for number
        if self.type == 'number':
            for key in ['decimalChar', 'groupChar', 'currency']:
                value = self.descriptor.get(key)
                if value is not None:
                    options[key] = value
        cast = getattr(types, 'cast_%s' % self.type)
        cast = partial(cast, self.format, **options)
        return cast

    def __get_check_functions(self):
        checks = {}
        cast = partial(self.cast_value, constraints=False)
        whitelist = _get_field_constraints(specs.table_schema, self.type)
        for name, constraint in self.constraints.items():
            if name in whitelist:
                # Cast enum constraint
                if name in ['enum']:
                    constraint = list(map(cast, constraint))
                # Cast maximum/minimum constraint
                if name in ['maximum', 'minimum']:
                    constraint = cast(constraint)
                check = getattr(constraints, 'check_%s' % name)
                checks[name] = partial(check, constraint)
        return checks


# Internal

def _get_field_constraints(spec, type):
    # Extract list of constraints for given type from jsonschema
    spec_types = spec['properties']['fields']['items']['anyOf']
    for spec_type in spec_types:
        if type in spec_type['properties']['type']['enum']:
            return spec_type['properties']['constraints']['properties'].keys()
