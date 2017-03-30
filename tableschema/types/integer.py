# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ..config import ERROR


# Module API

def cast_integer_default(value):
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except Exception:
        return ERROR
