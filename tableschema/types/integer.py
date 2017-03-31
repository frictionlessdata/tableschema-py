# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from ..config import ERROR


# Module API

def cast_integer(format, value):
    if not isinstance(value, int):
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = int(value)
        except Exception:
            return ERROR
    return value
