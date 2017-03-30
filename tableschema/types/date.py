# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from datetime import datetime, date
from dateutil.parser import parse
from ..config import ERROR


# Module API

def cast_date_default(value):
    PATTERN = '%Y-%m-%d'
    if not isinstance(value, date):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.strptime(value, PATTERN).date()
        except Exception:
            return ERROR
    return value


def cast_date_any(value):
    if not isinstance(value, date):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = parse(value).date()
        except Exception:
            return ERROR
    return value


def cast_date_pattern(value, pattern):
    if not isinstance(value, date):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = datetime.strptime(value, pattern).date()
        except Exception:
            return ERROR
    return value
