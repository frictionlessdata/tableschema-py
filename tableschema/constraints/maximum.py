# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_maximum(constraint, value):
    if value is None:
        return True
    if value <= constraint:
        return True
    return False
