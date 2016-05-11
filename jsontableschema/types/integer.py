# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import decimal
from future.utils import raise_with_traceback
from .. import exceptions
from .. import utilities
from . import base


# Module API

class IntegerType(base.JTSType):

    # Public

    name = 'integer'
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minimum',
        'maximum',
    ]
    null_values = utilities.NULL_VALUES
    # ---
    python_type = int

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return self.python_type(value)
        except (ValueError, TypeError, decimal.InvalidOperation) as e:
            raise_with_traceback(exceptions.InvalidCastError(e))

        raise exceptions.InvalidCastError('Could not cast value')
