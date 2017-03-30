# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import datetime
from dateutil.parser import parse
from ..config import ERROR


# Module API

def cast_datetime_default(value):
    PATTERN = '%Y-%m-%dT%H:%M:%SZ'
    if not isinstance(value, datetime.datetime):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.datetime.strptime(value, PATTERN)
        except Exception:
            return ERROR
    return value


def cast_datetime_pattern(value, pattern):
    if not isinstance(value, datetime.datetime):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.datetime.strptime(value, pattern)
        except Exception:
            return ERROR
    return value


def cast_datetime_any(value):
    if not isinstance(value, datetime.datetime):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = parse(value)
        except Exception:
            return ERROR
    return value
