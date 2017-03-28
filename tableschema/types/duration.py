# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import isodate
from future.utils import raise_with_traceback

from . import base
from .. import exceptions
from .. import helpers


# Module API

class DurationType(base.JTSType):
    # Public

    name = 'duration'
    null_values = helpers.NULL_VALUES
    supported_constraints = [
        'required',
        'unique',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = isodate.Duration
    formats = 'default'

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return isodate.parse_duration(value)
        except isodate.ISO8601Error as e:
            raise_with_traceback(exceptions.InvalidDurationType(e))
