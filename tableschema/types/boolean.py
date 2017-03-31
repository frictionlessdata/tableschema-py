# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
from ..config import ERROR


# Module API

def cast_boolean(format, value):
    TRUE_VALUES = ['yes', 'y', 'true', 't', '1']
    FALSE_VALUES = ['no', 'n', 'false', 'f', '0']
    if not isinstance(value, bool):
        if not isinstance(value, six.string_types):
            return ERROR
        value = value.strip().lower()
        if value in TRUE_VALUES:
            value = True
        elif value in FALSE_VALUES:
            value = False
        else:
            return ERROR
    return value
