# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions
from .. import utilities
from . import base


# Module API

class BooleanType(base.JTSType):

    # Public

    name = 'boolean'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
    ]
    # ---
    python_type = bool
    true_values = utilities.TRUE_VALUES
    false_values = utilities.FALSE_VALUES

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            value = value.strip().lower()
        except AttributeError:
            pass

        if value in (self.true_values):
            return True
        elif value in (self.false_values):
            return False
        else:
            raise exceptions.InvalidBooleanType(
                '{0} is not a boolean value'.format(value))
