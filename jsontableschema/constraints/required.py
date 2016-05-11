# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


# Module API

def check_required(name, value, required, null_values):
    """Required value constraint.

    Supported types: all.

    Args:
        name (str): field name
        value (str): field value
        null_values (str[]): list of null values

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """
    if required and value in null_values:
        message = 'The field "{0}" requires a value'
        message = message.format(name)
        raise exceptions.ConstraintError(message)
    return True
