# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
from decimal import Decimal
from ..config import ERROR


# Module API

def cast_number(format, value, **options):
    group_char = options.get('groupChar', _DEFAULT_GROUP_CHAR)
    decimal_char = options.get('decimalChar', _DEFAULT_DECIMAL_CHAR)
    if not isinstance(value, Decimal):
        if isinstance(value, six.string_types):
            value = re.sub(r'\s', '', value)
            value = value.replace(decimal_char, '.')
            value = value.replace(group_char, '')
            if not options.get('bareNumber', _DEFAULT_BARE_NUMBER):
                value = re.sub(r'((^\D*)|(\D*$))', '', value)
        elif not isinstance(value, six.integer_types + (float,)):
            return ERROR
        try:
            value = Decimal(value)
        except Exception:
            return ERROR
    return value


# Internal

_DEFAULT_GROUP_CHAR = ''
_DEFAULT_DECIMAL_CHAR = '.'
_DEFAULT_BARE_NUMBER = True
