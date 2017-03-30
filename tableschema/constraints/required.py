# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_required(value, required):
    """Required value constraint.

    Args:
        value (str): data value
        required (bool): is value required

    Returns:
        bool: constraint check result

    """
    if required and value is None:
        return False
    return True
