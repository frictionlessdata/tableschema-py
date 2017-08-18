# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
from ..config import ERROR


# Module API

def cast_integer(format, value, **options):
    if not isinstance(value, six.integer_types):
        if not isinstance(value, six.string_types):
            return ERROR
        if not options.get('bareNumber', _DEFAULT_BARE_NUMBER):
            value = re.sub(r'((^\D*)|(\D*$))', '', value)
        try:
            value = int(value)
        except Exception:
            return ERROR
    return value


# Internal

_DEFAULT_BARE_NUMBER = True
