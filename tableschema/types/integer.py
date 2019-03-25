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


def cast_integer(format, value, **options):
    if isinstance(value, six.integer_types):
        pass

    elif isinstance(value, six.string_types):
        if not options.get('bareNumber', _DEFAULT_BARE_NUMBER):
            value = re.sub(r'((^\D*)|(\D*$))', '', value)

        try:
            value = int(value)
        except Exception:
            return ERROR

    elif isinstance(value, float) and value.is_integer():
        value = int(value)

    elif isinstance(value, Decimal) and value % 1 == 0:
        value = int(value)

    else:
        return ERROR

    return value


# Internal

_DEFAULT_BARE_NUMBER = True
