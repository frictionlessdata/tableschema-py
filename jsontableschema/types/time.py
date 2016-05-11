# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import datetime
from future.utils import raise_with_traceback
from dateutil.parser import parse as date_parse
from .. import exceptions
from .. import utilities
from . import base


# Module API

class TimeType(base.JTSType):

    # Public

    name = 'time'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = datetime.time
    ISO8601 = '%H:%M:%S'
    raw_formats = ['HH/MM/SS']
    py_formats = ['%H:%M:%S']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            struct_time = time.strptime(value, self.ISO8601)
            return datetime.time(
                struct_time.tm_hour, struct_time.tm_min, struct_time.tm_sec)
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidTimeType(e))

    def cast_any(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return date_parse(value).time()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidTimeType(e))

    def cast_fmt(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return datetime.datetime.strptime(value, fmt).time()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidTimeType(e))
