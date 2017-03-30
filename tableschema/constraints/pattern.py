# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re


# Module API

def check_pattern(value, pattern):
    """Pattern constraint for a string value.

    Args:
        value (str): data value
        pattern (str): pattern to check

    Returns:
        bool: constraint check result

    """
    regex = re.compile('^{0}$'.format(pattern))
    match = regex.match(value)
    if not match:
        return False
    return True
