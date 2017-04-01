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

_DEFAULT_DECIMAL_CHAR = '.'
_DEFAULT_GROUP_CHAR = ''
_PERCENT_CHAR = '%‰‱％﹪٪'
_CURRENCIES = ''.join(compat.chr(i) for i in range(0xffff)
     if unicodedata.category(compat.chr(i)) == 'Sc')


def _preprocess_number(value, **options):
    currency = options.get('currency', False)
    group_char = options.get('groupChar', _DEFAULT_GROUP_CHAR)
    decimal_char = options.get('decimalChar', _DEFAULT_DECIMAL_CHAR)
    value = value.replace(decimal_char, '.')
    value = value.replace(group_char, '')
    value = re.sub('[' + _PERCENT_CHAR + ']', '', value)
    value = re.sub('\s', '', value)
    if currency:
        pattern = '[{0}]'.format(_CURRENCIES)
        value = re.sub(pattern, '', value)
    return value
