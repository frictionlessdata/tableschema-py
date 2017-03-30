# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
import uuid
import base64
import decimal
import rfc3986
import binascii
from ..config import ERROR


# Module API

def cast_string_default(value):
    if not isinstance(value, six.string_types):
        return ERROR
    return value


def cast_string_uri(value):
    if not isinstance(value, six.string_types):
        return ERROR
    if not rfc3986.is_valid_uri(value, require_scheme=True):
        return ERROR
    return value


def cast_string_email(value):
    PATTERN = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if not isinstance(value, six.string_types):
        return ERROR
    if not re.match(PATTERN, value):
        return ERROR
    return value


def cast_string_uuid(value):
    if not isinstance(value, six.string_types):
        return ERROR
    try:
        uuid.UUID(value, version=4)
    except ValueError:
        return ERROR
    return value


def cast_string_binary(value):
    if not isinstance(value, six.string_types):
        return ERROR
    try:
        base64.b64decode(value)
    except binascii.Error:
        return ERROR
    return value
