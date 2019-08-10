# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import namedtuple

import six

from ..config import ERROR

# Module API


def cast_yearmonth(format, value, **options):
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            return ERROR
        value = _yearmonth(value[0], value[1])
    elif isinstance(value, six.string_types):
        try:
            year, month = value.split('-')
            year = int(year)
            month = int(month)
            if (year < 0 or year > 9999) or (month < 1 or month > 12):
                return ERROR
            value = _yearmonth(year, month)
        except Exception:
            return ERROR
    else:
        return ERROR
    return value


def uncast_yearmonth(format, value, **options):
    if not (isinstance(value, (tuple, list)) and (len(value) == 2):
        return ERROR
    year, month=value
    if (year < 0 or year > 9999) or (month < 1 or month > 12):
        return ERROR
    return str(year).zfill(4) + '-' + str(month).zfill(2)


# Internal

_yearmonth=namedtuple('yearmonth', ['year', 'month'])
