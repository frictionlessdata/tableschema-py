# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
from .. import exceptions
from .. import utilities
from . import base


# Module API

class ArrayType(base.JTSType):

    # Public

    name = 'array'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minLength',
        'maxLength',
    ]
    # ---
    python_type = list

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            array_type = json.loads(value)
            if isinstance(array_type, self.python_type):
                return array_type
            else:
                raise exceptions.InvalidArrayType('Not an array')

        except (TypeError, ValueError):
            raise exceptions.InvalidArrayType(
                '"{0}" is not a array type'.format(value))
