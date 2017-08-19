# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from functools import partial
from .profile import Profile
from . import constraints
from . import exceptions
from . import helpers
from . import config
from . import types


# Module API

class Field(object):
    """Table Schema field representation.
    """

    # Public

    def __init__(self, descriptor, missing_values=config.DEFAULT_MISSING_VALUES):

        # Process descriptor
        descriptor = helpers.expand_field_descriptor(descriptor)

        # Set attributes
        self.__descriptor = descriptor
        self.__missing_values = missing_values
        self.__cast_function = self.__get_cast_function()
        self.__check_functions = self.__get_check_functions()

    @property
    def name(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.__descriptor.get('name')

    @property
    def type(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.__descriptor.get('type')

    @property
    def format(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.__descriptor.get('format')

    @property
    def required(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.constraints.get('required', False)

    @property
    def constraints(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.__descriptor.get('constraints', {})

    @property
    def descriptor(self):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        return self.__descriptor

    def cast_value(self, value, constraints=True):
        """https://github.com/frictionlessdata/tableschema-py#field
        """

        # Null value
        if value in self.__missing_values:
            value = None

        # Cast value
        cast_value = value
        if value is not None:
            cast_value = self.__cast_function(value)
            if cast_value == config.ERROR:
                raise exceptions.CastError((
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
                    raise exceptions.CastError((
                        'Field "{field.name}" has constraint "{name}" '
                        'which is not satisfied for value "{value}"'
                        ).format(field=self, name=name, value=value))

        return cast_value

    def test_value(self, value, constraints=True):
        """https://github.com/frictionlessdata/tableschema-py#field
        """
        try:
            self.cast_value(value, constraints=constraints)
        except exceptions.CastError:
            return False
        return True

    # Private

    def __get_cast_function(self):
        options = {}
        # Get cast options
        for key in ['decimalChar', 'groupChar', 'bareNumber', 'trueValues', 'falseValues']:
            value = self.descriptor.get(key)
            if value is not None:
                options[key] = value
        cast = getattr(types, 'cast_%s' % self.type)
        cast = partial(cast, self.format, **options)
        return cast

    def __get_check_functions(self):
        checks = {}
        cast = partial(self.cast_value, constraints=False)
        whitelist = _get_field_constraints(self.type)
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

def _get_field_constraints(type):
    # Extract list of constraints for given type from jsonschema
    jsonschema = Profile('table-schema').jsonschema
    profile_types = jsonschema['properties']['fields']['items']['anyOf']
    for profile_type in profile_types:
        if type in profile_type['properties']['type']['enum']:
            return profile_type['properties']['constraints']['properties'].keys()
