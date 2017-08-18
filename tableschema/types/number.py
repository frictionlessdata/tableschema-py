# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
import unicodedata
from decimal import Decimal
from .. import config


# Module API

def cast_number(format, value, **options):
    percentage = False
    currency = options.get('currency', False)
    group_char = options.get('groupChar', config.DEFAULT_NUMBER_GROUP_CHAR)
    decimal_char = options.get('decimalChar', config.DEFAULT_NUMBER_DECIMAL_CHAR)
    if not isinstance(value, Decimal):
        if isinstance(value, six.string_types):
            value = re.sub('\s', '', value)
            value = value.replace(decimal_char, '.')
            value = value.replace(group_char, '')
            result = re.sub('[' + _PERCENT_CHAR + ']', '', value)
            if value != result:
                value = result
                percentage = True
            if currency:
                pattern = '[{0}]'.format(_CURRENCIES)
                value = re.sub(pattern, '', value)
        elif not isinstance(value, six.integer_types + (float,)):
            return config.ERROR
        try:
            value = Decimal(value)
        except Exception:
            return config.ERROR
    if percentage:
        value = value/100
    return value


# Internal

_PERCENT_CHAR = '%‰‱％﹪٪'
_CURRENCIES = ''.join(six.unichr(i) for i in range(0xffff)
     if unicodedata.category(six.unichr(i)) == 'Sc')
