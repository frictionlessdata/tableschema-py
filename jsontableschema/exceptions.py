# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class InvalidSchemaError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'The obj is not a valid JSON Table Schema.'


class InvalidJSONError(Exception):
    def __init__(self, msg=None):
        self.msg = msg or 'The obj cannot be parsed as JSON.'


class InvalidCastError(Exception):
    pass


class RequiredFieldError(InvalidCastError):
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


class InvalidTimeType(InvalidCastError):
    pass


class InvalidGeoPointType(InvalidCastError):
    pass


class InvalidGeoJSONType(InvalidCastError):
    pass
