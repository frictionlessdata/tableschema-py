"""JTS type casting. Patterned on okfn/messy-tables"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import decimal
import datetime
import time
import json
from . import compat
from dateutil.parser import parse as date_parse


class JTSType(object):

    py = None

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        if value in ('', None):
            return False


class StringType(JTSType):

    py = compat.str

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        if value is None:
            return False
        if isinstance(value, self.py):
            return True
        return compat.str(value)


class IntegerType(JTSType):

    py = int

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(IntegerType, self).cast(value)
        if isinstance(value, self.py):
            return True
        try:
            return self.py(value)
        except ValueError:
            return False


class NumberType(JTSType):

    py = float, decimal.Decimal
    seperators = ',;'
    currencies = '$'

    def __init__(self, strip_seperators=False, strip_currencies=False):
        self.strip_seperators = strip_seperators
        self.strip_currencies = strip_currencies

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(NumberType, self).cast(value)
        if self.strip_seperators:
            value = re.sub('[{0}]'.format(self.seperators), '', value)
        if self.strip_currencies:
             value = re.sub('[{0}]'.format(self.currencies), '', value)
        if isinstance(value, self.py):
            return True
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            return False


class DateType(JTSType):

    py = datetime.date
    format = '%Y-%m-%d'

    def __init__(self, strict=False):
        self.strict = strict

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(DateType, self).cast(value)
        try:
            if self.strict:
                return datetime.datetime.strptime(value, self.format).date()
            else:
                return date_parse(value).date()
        except ValueError:
            return False


class TimeType(JTSType):

    py = time
    format = '%H:%M:%S'

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(TimeType, self).cast(value)
        try:
            return time.strptime(value, self.format)
        except ValueError:
            return False


class DateTimeType(JTSType):
    py = datetime.datetime
    format = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, strict=False):
        self.strict = strict

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(DateTimeType, self).cast(value)
        try:
            if self.strict:
                return datetime.datetime.strptime(value, self.format)
            else:
                return date_parse(value)
        except ValueError:
            return False


class BooleanType(JTSType):

    py = bool
    true_values = ('yes', 'y', 'true', '0')
    false_values = ('no', 'n','false', '1')

    def __init__(self, true_values=None, false_values=None):
        if true_values is not None:
            self.true_values = true_values
        if false_values is not None:
            self.false_values = false_values

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(BooleanType, self).cast(value)
        value = value.strip().lower()
        if value in self.true_values:
            return True
        if value in self.false_values:
            return False
        return False


class ArrayType(JTSType):

    py = list

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(ArrayType, self).cast(value)
        if isinstance(value, self.py):
            return True
        try:
            value = json.loads(value)
            if isinstance(value, self.py):
                return True
            else:
                return False
        except ValueError:
            return False


class ObjectType(JTSType):

    py = dict

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""
        super(ObjectType, self).cast(value)
        if isinstance(value, self.py):
            return True
        try:
            value = json.loads(value)
            if isinstance(value, self.py):
                return True
            else:
                return False
        except ValueError:
            return False


class AnyType(JTSType):

    def cast(self, value):
        return True
