# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import jsonschema.exceptions


# Base

class TableSchemaException(Exception):
    pass


class MultipleInvalid(TableSchemaException):
    def __init__(self, msg='Multiple errors found', errors=None):
        self.msg = msg
        if errors:
            self.errors = errors
        else:
            self.errors = []
        super(MultipleInvalid, self).__init__(msg)


# Load

class InvalidJSONError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'The obj cannot be parsed as JSON.'


# Validate

class InvalidSchemaError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'The obj is not a valid Table Schema.'


class SchemaValidationError(
        TableSchemaException,
        jsonschema.exceptions.ValidationError):
    pass


# Cast

class InvalidCastError(TableSchemaException):
    pass


class InvalidStringType(InvalidCastError):
    pass


class IncorrectTypeError(InvalidStringType):
    pass


class InvalidEmail(InvalidStringType):
    pass


class InvalidURI(InvalidStringType):
    pass


class InvalidBinary(InvalidStringType):
    pass


class InvalidUUID(InvalidStringType):
    pass


class InvalidNumberType(InvalidCastError):
    pass


class InvalidCurrency(InvalidNumberType):
    pass


class InvalidBooleanType(InvalidCastError):
    pass


class InvalidNoneType(InvalidCastError):
    pass


class InvalidObjectType(InvalidCastError):
    pass


class InvalidArrayType(InvalidCastError):
    pass


class InvalidDateType(InvalidCastError):
    pass


class InvalidDateTimeType(InvalidCastError):
    pass


class InvalidYearType(InvalidCastError):
    pass


class InvalidYearMonthType(InvalidCastError):
    pass


class InvalidDurationType(InvalidCastError):
    pass


class InvalidTimeType(InvalidCastError):
    pass


class InvalidGeoPointType(InvalidCastError):
    pass


class InvalidGeoJSONType(InvalidCastError):
    pass


# Constraints

class ConstraintError(TableSchemaException):
    def __init__(self, msg=None):
        self.msg = msg or 'The value didn\'t validate against a constraint.'
        super(ConstraintError, self).__init__(msg)


class ConstraintNotSupported(TableSchemaException):
    def __init__(self, msg=None):
        self.msg = msg or 'The field does not support the constraint.'
        super(ConstraintNotSupported, self).__init__(msg)


# Storage

class StorageError(TableSchemaException):
    pass


# Deprecated

class ConversionError(TableSchemaException):
    def __init__(self, msg=None):
        self.msg = msg or 'Error converting a row or field.'
        super(ConversionError, self).__init__(msg)
