# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import utilities
from . import base


# Module API

class AnyType(base.JTSType):

    # Public

    name = 'any'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
    ]

    def cast_default(self, value, fmt=None):
        return value
