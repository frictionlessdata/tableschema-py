# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re


# Module API

def check_pattern(value, pattern):
    regex = re.compile('^{0}$'.format(pattern))
    match = regex.match(value)
    if not match:
        return False
    return True
