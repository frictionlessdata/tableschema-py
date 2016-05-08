# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import decimal
import unicodedata
from future.utils import raise_with_traceback
from .. import exceptions
from .. import compat
from .. import utilities
from . import base


# Module API

class NumberType(base.JTSType):

    # Public

    name = 'number'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = decimal.Decimal
    separators = ',; '
    currencies = u''.join(compat.chr(i) for i
                          in range(0xffff)
                          if unicodedata.category(compat.chr(i)) == 'Sc')


    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return self.python_type(value)
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise_with_traceback(exceptions.InvalidCastError(e))

        raise exceptions.InvalidCastError('Could not cast value')

    def cast_currency(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        if isinstance(value, (int, float)):
            return self.python_type(value)

        try:
            pattern = '[{0}{1}]'.format(self.separators, self.currencies)
            value = re.sub(pattern, '', value)
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            raise exceptions.InvalidCurrency(
                '{0} is not a valid currency'.format(value))

        raise exceptions.InvalidCastError('Could not cast value')
