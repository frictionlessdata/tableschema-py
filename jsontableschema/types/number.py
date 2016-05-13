# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import decimal
import unicodedata
import six
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
    # TODO: Change this initialization to something more performant (http://bit.ly/1qgkK7B)
    currencies = u''.join(compat.chr(i) for i
                          in range(0xffff)
                          if unicodedata.category(compat.chr(i)) == 'Sc')

    def __preprocess_value(self, value):
        if type(value) is six.text_type:
            group_char = self.field.get('groupChar', ',')
            decimal_char = self.field.get('decimalChar', '.')
            value = value.replace(group_char, '').replace(decimal_char, '.')
        return value

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        if isinstance(value, (int, float)):
            return self.python_type(value)

        value = self.__preprocess_value(value)

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

        value = self.__preprocess_value(value)

        try:
            pattern = '[{0}]'.format(self.currencies)
            value = re.sub(pattern, '', value)
            return self.python_type(value)
        except (ValueError, TypeError, decimal.InvalidOperation):
            raise exceptions.InvalidCurrency(
                '{0} is not a valid currency'.format(value))

        raise exceptions.InvalidCastError('Could not cast value')
