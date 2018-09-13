# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

class DataPackageException(Exception):

    # Public

    def __init__(self, message, errors=[], **metadata):
        self.__errors = errors
        self.__metadata = metadata
        super(Exception, self).__init__(message)

    @property
    def multiple(self):
        return bool(self.__errors)

    @property
    def errors(self):
        return self.__errors

    @property
    def metadata(self):
        return self.__metadata


class TableSchemaException(DataPackageException):
    pass


class LoadError(TableSchemaException):
    pass


class ValidationError(TableSchemaException):
    pass


class CastError(TableSchemaException):
    pass


class RelationError(TableSchemaException):
    pass


class StorageError(TableSchemaException):
    pass


# Deprecated

MultipleInvalid = TableSchemaException
InvalidJSONError = LoadError
SchemaValidationError = ValidationError
InvalidSchemaError = ValidationError
InvalidCastError = CastError
ConstraintError = CastError
