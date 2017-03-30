# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_minimum(value, minimum):
    """Minimum and maximum constraint.

    Args:
        value (int/float/Decimal/datetime/date/time): data value
        minimum (int/float/Decimal/datetime/date/time): minimum to check

    Returns:
        bool: constraint check result

    """
    if value < minimum:
        return False
    return True
