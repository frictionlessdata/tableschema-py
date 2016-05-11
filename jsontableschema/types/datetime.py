# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from future.utils import raise_with_traceback
from dateutil.parser import parse as date_parse
from .. import exceptions
from .. import utilities
from . import base


# Module API

class DateTimeType(base.JTSType):

    # Public

    name = 'datetime'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = datetime.datetime
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
    raw_formats = ['DD/MM/YYYYThh/mm/ss']
    py_formats = ['%Y/%m/%dT%H:%M:%S']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return datetime.datetime.strptime(value, self.ISO8601)
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateTimeType(e))

    def cast_any(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return date_parse(value)
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateTimeType(e))

    def cast_fmt(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return datetime.datetime.strptime(value, fmt)
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateTimeType(e))
