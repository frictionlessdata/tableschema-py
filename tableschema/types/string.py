# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
import uuid
import base64
import rfc3986
from ..config import ERROR


# Module API

def cast_string(format, value):
    if not isinstance(value, six.string_types):
        return ERROR
    if format == 'uri':
        if not rfc3986.is_valid_uri(value, require_scheme=True):
            return ERROR
    elif format == 'email':
        if not re.match(_EMAIL_PATTERN, value):
            return ERROR
    elif format == 'uuid':
        try:
            uuid.UUID(value, version=4)
        except Exception:
            return ERROR
    elif format == 'binary':
        try:
            base64.b64decode(value)
        except Exception:
            return ERROR
    return value


# Internal

_EMAIL_PATTERN = re.compile(r'[^@]+@[^@]+\.[^@]+')
