# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re
from decimal import Decimal

import six

from ..config import ERROR

_format = format

# Module API


def cast_number(format, value, **options):
    group_char = options.get('groupChar', _DEFAULT_GROUP_CHAR)
    decimal_char = options.get('decimalChar', _DEFAULT_DECIMAL_CHAR)
    if not isinstance(value, Decimal):
        if isinstance(value, six.string_types):
            value = re.sub(r'\s', '', value)
            value = value.replace(decimal_char, '__decimal_char__')
            value = value.replace(group_char, '')
            value = value.replace('__decimal_char__', '.')
            if not options.get('bareNumber', _DEFAULT_BARE_NUMBER):
                value = re.sub(r'((^\D*)|(\D*$))', '', value)
        elif not isinstance(value, six.integer_types + (float,)):
            return ERROR
        try:
            if isinstance(value, float):
                value = str(value)
            value = Decimal(value)
        except Exception:
            return ERROR
    return value


def uncast_number(format, value, **options):
    if not isinstance(value, Decimal):
        return ERROR
    group_char = options.get('groupChar', _DEFAULT_GROUP_CHAR)
    decimal_char = options.get('decimalChar', _DEFAULT_DECIMAL_CHAR)
    if group_char:
        uncast = _format(value, '03,').replace(',', group_char)
    else:
        uncast = str(value)
    if decimal_char != '.':
        uncast = uncast.replace('.', decimal_char)
    return uncast


# Internal

_DEFAULT_GROUP_CHAR = ''
_DEFAULT_DECIMAL_CHAR = '.'
_DEFAULT_BARE_NUMBER = True
