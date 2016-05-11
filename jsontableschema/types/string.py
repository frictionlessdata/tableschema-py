# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import uuid
import base64
import decimal
import binascii
from rfc3986 import is_valid_uri
from future.utils import raise_with_traceback
from .. import exceptions
from .. import compat
from .. import utilities
from . import base


# Module API

class StringType(base.JTSType):

    # Public

    name = 'string'
    null_values = [value for value in utilities.NULL_VALUES if value != '']
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minLength',
        'maxLength',
    ]
    # ---
    python_type = compat.str
    email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')

    def cast_default(self, value, fmt=None):

        if not isinstance(value, self.python_type):
            raise exceptions.InvalidStringType(
                '{0} is not of type {1}'.format(value, self.python_type))

        try:
            return self.python_type(value)
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise_with_traceback(exceptions.InvalidCastError(e))

        raise exceptions.InvalidCastError('Could not cast value')

    def cast_email(self, value, fmt=None):

        if not isinstance(value, self.python_type):
            raise exceptions.InvalidStringType(
                '{0} is not of type {1}'.format(value, self.python_type))

        if not re.match(self.email_pattern, value):
            raise exceptions.InvalidEmail(
                '{0} is not a valid email'.format(value))

        return value

    def cast_uri(self, value, fmt=None):

        if not isinstance(value, self.python_type):
            raise exceptions.InvalidStringType(
                '{0} is not of type {1}'.format(value, self.python_type))

        if is_valid_uri(value, require_scheme=True):
            return value
        else:
            raise exceptions.InvalidURI(
                '{0} is not a valid uri'.format(value))

    def cast_binary(self, value, fmt=None):

        if not isinstance(value, self.python_type):
            raise exceptions.InvalidStringType(
                '{0} is not of type {1}'.format(value, self.python_type))

        try:
            base64.b64decode(value)
        except binascii.Error as e:
            raise_with_traceback(exceptions.InvalidBinary(e))
        return value

    def cast_uuid(self, value, fmt=None):

        if not isinstance(value, self.python_type):
            raise exceptions.InvalidStringType(
                '{0} is not of type {1}'.format(value, self.python_type))

        try:
            uuid.UUID(value, version=4)
            return value
        except ValueError as e:
            raise_with_traceback(exceptions.InvalidUUID(e))
