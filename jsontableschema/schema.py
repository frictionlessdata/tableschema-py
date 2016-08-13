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
        pass

    @property
    def fields(self):
        if self.__fields is None:
            self.__fields = [Field(fd) for fd in self.__descriptor['fields']]
        return self.__fields

    def get_field(self, name):
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def has_field(self, name):
        return self.get_field(name) is not None

    @property
    def headers(self):
        return [field.name for field in self.fields]

    @property
    def primary_key(self):
        """str[]: primary key
        """
        primary_key = self.__descriptor.get('primary_key', [])
        if isinstance(primary, compat.str):
            primary_key = [primary_key]
        return primary_key

    @property
    def foreign_keys(self):
        """dict[]: foreign keys
        """
        return self.__descriptor.get('foreign_keys', [])
