# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import decimal

from future.utils import raise_with_traceback

from . import base
from .. import exceptions
from .. import helpers


# Module API

class YearType(base.JTSType):
    # Public

    name = 'year'
    null_values = helpers.NULL_VALUES
    supported_constraints = [
        'required',
        'unique',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = int
    formats = 'default'

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        if len(value) > 4:
            raise exceptions.InvalidYearType(
                '{0} is not a valid year value'.format(value))

        try:
            return self.python_type(value)
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise_with_traceback(exceptions.InvalidYearType(e))
