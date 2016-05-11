# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


# Module API

def check_maxLength(name, value, max_length):
    """Length constraint.

    Supported types: sting, array, object.

    Args:
        name (str): field name
        value (str/list/dict): field value
        max_length (str/list/dict): max length to check

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """
    if len(value) > max_length:
        raise exceptions.ConstraintError(
            "The field '{0}' must have a maximum length of {1}"
            .format(name, max_length))
    return True
