# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_enum(value, enum):
    if value not in enum:
        return False
    return True
