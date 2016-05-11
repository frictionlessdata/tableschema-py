# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, date, time
from dateutil.parser import parse as date_parse
from .. import exceptions


# Module API

def check_minimum(name, value, minimum):
    """Minimum and maximum constraint.

    Supported types: integer, number, datetime, date, time.

    Args:
        name (str): field name
        value (int/float/Decimal/datetime/date/time): field value
        minimum (int/float/Decimal/datetime/date/time): minimum to check

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """
    if value < minimum:
        raise exceptions.ConstraintError(
            "The field '{0}' must not be less than {1}"
            .format(name, minimum))
    return True
