# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
import unicodedata
from decimal import Decimal
from ..config import ERROR
from .. import compat


# Module API

def cast_number(format, value, **options):
    if not isinstance(value, Decimal):
        if isinstance(value, six.string_types):
            value = _preprocess_number(value, **options)
        elif not isinstance(value, (int, float)):
            return ERROR
        try:
            value = Decimal(value)
        except Exception:
            return ERROR
    return value


# Internal

_CURRENCIES = ''.join(compat.chr(i) for i in range(0xffff)
     if unicodedata.category(compat.chr(i)) == 'Sc')


def _preprocess_number(value, **options):
    percent_char = '%‰‱％﹪٪'
    group_char = options.get('groupChar', ',')
    decimal_char = options.get('decimalChar', '.')
    currency = options.get('currency', False)
    value = value.replace(group_char, '').replace(decimal_char, '.')
    value = re.sub('['+percent_char+']', '', value)
    value = re.sub('\s', '', value)
    if currency:
        pattern = '[{0}]'.format(_CURRENCIES)
        value = re.sub(pattern, '', value)
    return value
