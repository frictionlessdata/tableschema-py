# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import deepcopy
from .field import Field
from .validate import validate, validator
from . import compat
from . import exceptions
from . import utilities


# Module API

class Schema(object):
    """JSON Table Schema schema representation.

    Raises:
        exceptions.InvalidJSONError

    Args:
        descriptor (dict/str): schema descriptor/path/url

    """

    # Public

    def __init__(self, descriptor):
        self.__descriptor = deepcopy(utilities.load_json_source(descriptor))
        self.__fields = None

    @property
    def descriptor(self):
        """dict: schema descriptor
        """
        return self.__descriptor

    def validate(self, fail_fast=False):
        """Validate schema descriptor.

        Args:
            fail_fast (bool): raise first error

        Raises:
            exceptions.InvalidSchemaError
            exceptions.MultipleInvalid

        Returns:
            bool: True if valid

        """
        # Raise first error
        if fail_fast:
            try:
                validate(self.__descriptor)
            except exceptions.SchemaValidationError:
                raise exceptions.InvalidSchemaError
        # Raise all errors
        else:
            errors = list(validator.iter_errors(self.__descriptor))
            if errors:
                raise exceptions.MultipleInvalid(errors=errors)
        return True

    def convert_row(self, row, fail_fast=False):
        """Convert row to schema types.

        Args:
            row (mixed[]): array of values
            fail_fast (bool): raise first occured error

        Raises:
            exceptions.ConversionError
            exceptions.MultipleInvalid

        Returns:
            mixed[]: converted row

        """
        # Check row length
        if len(row) != len(self.fields):
            message = 'Row length (%s) doesn\'t match fields count (%s)'
            message = message % (len(row), len(self.fields))
            raise exceptions.ConversionError(message)

        # Convert
        result = []
        errors = []
        for field, value in zip(self.fields, row):
            try:
                result.append(field.convert_value(value))
            except exceptions.InvalidCastError as exception:
                if fail_fast:
                    raise
                errors.append(exception)

        # Raise errors
        if errors:
            raise exceptions.MultipleInvalid(errors=errors)

        return result

    @property
    def fields(self):
        """Field[]: field instances
        """
        if self.__fields is None:
            self.__fields = [Field(fd) for fd in self.__descriptor['fields']]
        return self.__fields

    def get_field(self, name):
        """Return field by name.

        Args:
            name (str): field name

        Returns:
            None/Field: return field instance or
                None if field with name doesn't exist

        """
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def has_field(self, name):
        """Check if field exists.

        Args:
            name (str): field name

        Returns:
            bool: existence of field

        """
        return self.get_field(name) is not None

    @property
    def headers(self):
        """str[]: field names (headers)
        """
        return [field.name for field in self.fields]

    @property
    def primary_key(self):
        """str[]: primary key
        """
        primary_key = self.__descriptor.get('primaryKey', [])
        if isinstance(primary_key, compat.str):
            primary_key = [primary_key]
        return primary_key

    @property
    def foreign_keys(self):
        """dict[]: foreign keys
        """
        return self.__descriptor.get('foreignKeys', [])
