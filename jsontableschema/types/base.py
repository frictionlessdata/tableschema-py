# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from functools import partial
from abc import ABCMeta, abstractmethod
import six
from .. import compat
from .. import exceptions
from .. import constraints


# Module API

class JTSType(object):
    """Base class for all JSON Table Schema types.

    Args:
        field (dict): field schema

    Aside implementing `cast_default` subclass could add other cast methods
    with the same signature like `cast_fmt`, `cast_current` etc
    to add support for corresponding formats.

    """

    # Public

    @property
    @abstractmethod
    def name(self):
        """str: type name like `array`
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def null_values(self):
        """str[]: list of strings to process as null value
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def supported_constraints(self):
        """str[]: list of supported JTS constraints
        """
        pass  # pragma: no cover

    def __init__(self, field=None):

        # Set default field
        self.__field = {}
        self.__field_name = None
        self.__format = 'default'
        self.__constraints = {}

        # Set user defined field
        if field:
            self.__field = field
            self.__field_name = field['name']
            self.__format = field['format']
            self.__constraints = field.get('constraints', {})

        # Set parsed format (fmt feature)
        self.__format_main = self.__format
        self.__format_fmt = None
        if self.__format.startswith('fmt'):
            self.__format_main = 'fmt'
            self.__format_fmt = self.__format.strip('fmt:')

    @property
    def field(self):
        """Returns original field object for this type
        Should be used for getting extra properties for this type
        """
        return self.__field

    def cast(self, value, skip_constraints=False):
        """Cast value.

        Args:
            value (any): value to cast
            skip_constraints (bool): if True it skips constraints checks

        Returns:
           any: cast value

        """

        # If value is null
        if self.__is_null(value):

            # Check required constraint
            if not skip_constraints:
                required = self.__constraints.get('required', False)
                constraints.check_required(self.__field_name, value, required,
                    self.null_values+[None])

            return None

        # Check pattern constraint
        if not skip_constraints:
            # Only if value not cast
            if isinstance(value, compat.str):
                pattern = self.__constraints.get('pattern', None)
                if pattern is not None:
                    constraints.check_pattern(
                        self.__field_name, value, pattern)

        # Cast value
        cast_name = 'cast_%s' % self.__format_main
        cast_func = getattr(self, cast_name, self.cast_default)
        cast_value = cast_func(value, self.__format_fmt)

        # Check against post-cast constraints
        if not skip_constraints:
            for check_name, check_value in self.__constraints.items():
                # We can't handle unique constraint on this level
                # (shouldn't be added to supported_constraints in subclass)
                if check_name in ['unique']:
                    continue
                if check_name in ['required', 'pattern']:
                    continue
                if check_name not in self.supported_constraints:
                    raise exceptions.ConstraintNotSupported(
                        "Field type '{0}' does not support the {1} constraint"
                        .format(self.name, check_name))
                if check_name in ['minimum', 'maximum']:
                    check_value = self.cast(check_value, skip_constraints=True)
                if check_name in ['enum']:
                    mapper = partial(self.cast, skip_constraints=True)
                    check_value = map(mapper, check_value)
                check_func = getattr(constraints, 'check_%s' % check_name)
                check_func(self.__field_name, cast_value, check_value)

        return cast_value

    def test(self, value):
        """Test value could be cast.

        Args:
            value (any): value to check

        Returns:
            bool: could be cast

        """
        try:
            self.cast(value)
            return True
        except exceptions.InvalidCastError:
            return False

    @abstractmethod
    def cast_default(self, value, fmt=None):
        """Cast default.

        Args:
            value (any): value to cast
            format (str): secondary format (JTS's "fmt")

        """
        pass  # pragma: no cover

    # Private

    def __is_null(self, value):
        """Check for null value.
        If value is string-like, will strip it before testing.

        Args:
            value (any): value to test for nullity

        Returns:
            true if a null value

        """
        if type(value) in six.string_types or type(value) is six.text_type:
            value = value.strip()
        return value in self.null_values + [None]
