# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def check_minimum(value, minimum):
    if value < minimum:
        return False
    return True
