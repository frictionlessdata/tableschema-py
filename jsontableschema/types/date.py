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

class DateType(base.JTSType):

    # Public

    name = 'date'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minimum',
        'maximum',
    ]
    # ---
    python_type = datetime.date
    formats = ('default', 'any', 'fmt')
    ISO8601 = '%Y-%m-%d'
    raw_formats = ['DD/MM/YYYY', 'DD/MM/YY', 'YYYY/MM/DD']
    py_formats = ['%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return datetime.datetime.strptime(value, self.ISO8601).date()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateType(e))

    def cast_any(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return date_parse(value).date()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateType(e))

    def cast_fmt(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            return datetime.datetime.strptime(value, fmt).date()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidDateType(e))
