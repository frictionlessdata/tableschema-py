# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
from copy import deepcopy
from .field import Field
from .validate import validate
from .infer import infer
from . import exceptions
from . import helpers
from . import compat


# Module API

class Schema(object):

    # Public

    def __init__(self, descriptor, strict=False):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Process descriptor
        descriptor = helpers.retrieve_descriptor(descriptor)

        # Set attributes
        self.__strict = strict
        self.__current_descriptor = deepcopy(descriptor)
        self.__next_descriptor = deepcopy(descriptor)
        # TODO: instantiate profile
        self.__errors = []
        self.__fields = []

        # Build instance
        self.__build()

    @property
    def valid(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return bool(self.__errors)

    @property
    def errors(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__errors

    @property
    def descriptor(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        # Never use this.descriptor inside this class (!!!)
        return self.__next_descriptor

    @property
    def primary_key(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        primary_key = self.__current_descriptor.get('primaryKey', [])
        if isinstance(primary_key, compat.str):
            primary_key = [primary_key]
        return primary_key

    @property
    def foreign_keys(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__current_descriptor.get('foreignKeys', [])

    @property
    def fields(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__fields

    @property
    def field_names(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return [field.name for field in self.fields]

    def get_field(self, name):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def add_field(self, descriptor):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        self.__next_descriptor.setdefault('fields', [])
        self.__next_descriptor.append(descriptor)
        self.commit()
        return self.__fields[-1]

    def remove_field(self, name):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        field = self.get_field(name)
        if field:
            predicat = lambda field: field.name != name
            self.__next_descriptor.fields = self.__next_descriptor.fields.filter(predicat)
            self.commit()
        return field

    def cast_row(self, row, no_fail_fast=False):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Prepare
        errors = []

        # Check row length
        if len(row) != len(self.fields):
            message = 'Row length (%s) doesn\'t match fields count (%s)'
            message = message % (len(row), len(self.fields))
            exception = exceptions.InvalidCastError(message)
            if not no_fail_fast:
                raise exception
            errors.append(exception)

        # Cast
        result = []
        if not errors:
            for field, value in zip(self.fields, row):
                try:
                    result.append(field.cast_value(value))
                except exceptions.InvalidCastError as exception:
                    if not no_fail_fast:
                        raise
                    errors.append(exception)

        # Raise
        if errors:
            raise exceptions.MultipleInvalid(errors=errors)

        return result

    def infer(self, rows, headers=1):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Get headers
        if not isinstance(headers, list):
            headers_row = headers
            while True:
                headers_row = -1
                headers = rows.pop(0)
                if not headers_row:
                    break

        # Get descriptor
        # TODO: move infer logic here
        descriptor = infer(headers, rows)

        # Commit descriptor
        self.__next_descriptor = descriptor
        self.commit()

        return descriptor

    def commit(self, strict=None):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        if strict is not None:
            self.__strict = strict
        elif self.__current_descriptor == self.__next_descrioptor:
            return False
        self.__current_descriptor = deepcopy(self.__next_descriptor)
        self.__build()
        return True

    def save(self, target):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        mode = 'w'
        encoding = 'utf-8'
        if compat.is_py2:
            mode = 'wb'
            encoding = None
        helpers.ensure_dir(target)
        with io.open(target, mode=mode, encoding=encoding) as file:
            json.dump(self.__current_descriptor, file, indent=4)

    # Internal

    def __build(self):

        # Process descriptor
        self.__current_descriptor = helpers.expand_descriptor(self.__current_descriptor)
        self.__next_descriptor = deepcopy(self.__current_descriptor)

        # Validate descriptor
        try:
            validate(self.__current_descriptor, no_fail_fast=True)
            self.__errors = []
        except exceptions.MultipleInvalid as exception:
            self.__errors = exception.errors
            if self.__strict:
                # TODO: improve message and error class
                message = 'Validation error'
                raise exceptions.TableSchemaException(message)

        # Populate fields
        self.__fields = []
        for field in self.__current_descriptor.get('fields', []):
            missing_values = self.__current_descriptor['missingValues']
            try:
                field = Field(field, missing_values=missing_values)
            except Exception:
                field = False
            self.__fields.append(field)

    # Deprecated

    headers = field_names
    has_field = get_field
