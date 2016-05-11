# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import exceptions
from .. import compat


# Module API

def check_pattern(name, value, pattern):
    """Pattern constraint for a string value.

    Supported types: all.
    Input arguments should NOT be casted to type.
    Pattern constraint should be checked as a string value before the value
    is cast. `value` is treated as a string and must match the XML Schema Reg
    Exp `pattern`.

    Args:
        name (str): field name
        value (str): field value
        pattern (str): pattern to check

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """

    # Convert to str if necessary
    if not isinstance(value, compat.str):
        value = compat.str(value)

    # Check constaint
    regex = re.compile('^{0}$'.format(pattern))
    match = regex.match(value)
    if not match:
        raise exceptions.ConstraintError(
            "The value for field '{0}' must match the pattern"
            .format(name))

    return True
