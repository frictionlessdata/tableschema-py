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

def cast_time(format, value):
    PATTERN = '%H:%M:%S'
    if not isinstance(value, time):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            if format == 'default':
                value = datetime.strptime(value, PATTERN).time()
            elif format == 'any':
                value = parse(value).time()
            else:
                value = datetime.strptime(value, format).time()
        except Exception:
            return ERROR
    return value
