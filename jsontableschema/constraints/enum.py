# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


# Module API

def check_enum(name, value, enum):
    """Enum constraint.

    Check value is one from enumerable type.

    Args:
        name (str): field name
        value (any): field value
        enum (any[]): enum to check against

    Raises:
        TypeError: for non supported type
        ConstraintError: if check is failed

    """
    if value not in enum:
        raise exceptions.ConstraintError(
            "The value for field '{0}' must be in the enum array"
            .format(name))
    return True
