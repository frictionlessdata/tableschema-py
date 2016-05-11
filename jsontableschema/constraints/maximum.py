# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, date, time
from dateutil.parser import parse as date_parse
from .. import exceptions


# Module API

def check_maximum(name, value, maximum):
    """Minimum and maximum constraint.

    Supported types: integer, number, datetime, date, time.

    Args:
        name (str): field name
        value (int/float/Decimal/datetime/date/time): field value
        maximum (int/float/Decimal/datetime/date/time): maximum to check

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """
    if value > maximum:
        raise exceptions.ConstraintError(
            "The field '{0}' must not be more than {1}"
            .format(name, maximum))
    return True
