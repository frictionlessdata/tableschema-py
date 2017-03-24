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

class YearMonthType(base.JTSType):
    # Public

    name = 'yearmonth'
    null_values = helpers.NULL_VALUES
    supported_constraints = [
        'required',
        'unique',
        'pattern',
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

        try:
            cast_value = self.python_type(value)
            if not (1 <= cast_value <= 12):
                raise exceptions.InvalidYearMonthType(
                    '{0} is not a valid yearmonth value'.format(value))
            return cast_value
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise_with_traceback(exceptions.InvalidYearMonthType(e))
