# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from datetime import datetime, time
from dateutil.parser import parse
from ..config import ERROR


# Module API

def cast_time_default(value):
    PATTERN = '%H:%M:%S'
    if not isinstance(value, time):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.strptime(value, PATTERN).time()
        except Exception:
            return ERROR
    return value


def cast_time_any(value):
    if not isinstance(value, time):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = parse(value).time()
        except Exception:
            return ERROR
    return value


def cast_time_pattern(value, pattern):
    if not isinstance(value, time):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.strptime(value, pattern).time()
        except Exception:
            return ERROR
    return value
