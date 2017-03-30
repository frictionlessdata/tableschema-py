# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_maxLength(value, maxLength):
    """Length constraint.

    Args:
        value (str/list/dict): data value
        maxLength (int): max length to check

    Returns:
        bool: constraint check result

    """
    if len(value) > maxLength:
        return False
    return True
