# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import six
from decimal import Decimal
from .. import config


# Module API

def cast_number(format, value, **options):
    group_char = options.get('groupChar', config.DEFAULT_NUMBER_GROUP_CHAR)
    decimal_char = options.get('decimalChar', config.DEFAULT_NUMBER_DECIMAL_CHAR)
    if not isinstance(value, Decimal):
        if isinstance(value, six.string_types):
            value = re.sub('\s', '', value)
            value = value.replace(decimal_char, '.')
            value = value.replace(group_char, '')
            if not options.get('bareNumber', config.DEFAULT_NUMBER_BARE_NUMBER):
                value = re.sub(r'((^\D*)|(\D*$))', '', value)
        elif not isinstance(value, six.integer_types + (float,)):
            return config.ERROR
        try:
            value = Decimal(value)
        except Exception:
            return config.ERROR
    return value
