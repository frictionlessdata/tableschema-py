# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from datetime import datetime
from dateutil.parser import parse
from ..config import ERROR


# Module API

def cast_datetime(format, value):
    if not isinstance(value, datetime):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            if format == 'default':
                PATTERN = '%Y-%m-%dT%H:%M:%SZ'
                value = datetime.strptime(value, PATTERN)
            elif format == 'any':
                value = parse(value)
            else:
                value = datetime.strptime(value, format)
        except Exception:
            return ERROR
    return value
