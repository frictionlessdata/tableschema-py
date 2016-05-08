# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions
from .. import utilities
from . import base


# Module API

class NullType(base.JTSType):

    # Public

    name = 'null'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
    ]
    # ---
    python_type = type(None)

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        value = value.strip().lower()
        if value in self.null_values:
            return None
        else:
            raise exceptions.InvalidNoneType(
                '{0} is not a none type'.format(value))
