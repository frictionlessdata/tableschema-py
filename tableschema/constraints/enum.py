# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_enum(value, enum):
    """Enum constraint.

    Args:
        value (any): data value
        enum (any[]): enum to check against

    Returns:
        bool: constraint check result

    """
    if value not in enum:
        return False
    return True
