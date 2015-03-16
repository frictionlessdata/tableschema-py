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
import operator
import base64
import binascii
from dateutil.parser import parse as date_parse
from . import compat
from . import utilities


class JTSType(object):

    """Base class for all JSON Table Schema types."""

    py = type(None)
    name = ''
    formats = ('default',)

    def __init__(self, field=None, **kwargs):
        """Setup some variables for easy access. `field` is the field schema."""

        self.field = field

        if self.field:
            self.format = self.field['format']
            self.required = self.field['constraints']['required']
        else:
            self.format = 'default'
            self.required = True

    def cast(self, value):
        """Return boolean if `value` can be cast as type `self.py`."""

        # we can check on `constraints.required` before we cast
        if not self.required and (value in (None, utilities.NULL_VALUES)):
            return True

        elif self.required and value in (None, ''):
            return False

        # cast with the appropriate handler, falling back to default if none

        if self.format.startswith('fmt'):
            _format = 'fmt'
        else:
            _format = self.format

        _handler = 'cast_{0}'.format(_format)

        if self.has_format(_format) and hasattr(self, _handler):
            return getattr(self, _handler)(value)

        return self.cast_default(value)

    def cast_default(self, value):
        """Return boolean if the value can be cast to the type/format."""

        if self._type_check(value):
            return value

        try:
            if not self.py == compat.str:
                return self.py(value)

        except (ValueError, TypeError, decimal.InvalidOperation):
            return False

        return False

    def has_format(self, _format):

        if _format in self.formats:
            return True

        return False

    def _type_check(self, value):
        """Return boolean on type check of value. """

        if isinstance(value, self.py):
            return True

        return False


class StringType(JTSType):

    py = compat.str
    name = 'string'
    formats = ('default', 'email', 'uri', 'binary')
    email_pattern = re.compile(r'[^@]+@[^@]+\.[^@]+')
    # TODO: this is not a URI pattern
    uri_pattern = re.compile(r'^http[s]?://')

    def cast_email(self, value):
        """Return `value` if is of type, else return False."""

        if not self._type_check(value):
            return False

        if not re.match(self.email_pattern, value):
            return False

        return value

    def cast_uri(self, value):
        """Return `value` if is of type, else return False."""

        if not self._type_check(value):
            return False

        if not re.match(self.uri_pattern, value):
            return False

        return value

    def cast_binary(self, value):
        """Return `value` if is of type, else return False."""

        if not self._type_check(value):
            return False

        try:
            base64.b64decode(value)
        except binascii.Error as e:
            return False

        return True


class IntegerType(JTSType):

    py = int
    name = 'integer'


class NumberType(JTSType):

    py = decimal.Decimal
    name = 'number'
    formats = ('default', 'currency')
    separators = ',;'
    currencies = '$'

    def cast_currency(self, value):
        value = re.sub('[{0}{1}]'.format(self.separators, self.currencies), '', value)

        if isinstance(value, self.py):
            return True

        try:
            return decimal.Decimal(value)

        except decimal.InvalidOperation:
            return False


class BooleanType(JTSType):

    py = bool
    name = 'boolean'
    true_values = utilities.TRUE_VALUES
    false_values = utilities.FALSE_VALUES

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        if isinstance(value, self.py):
            return True

        else:

            value = value.strip().lower()
            if value in (self.true_values + self.false_values):
                return True

            return False


class NullType(JTSType):

    py = type(None)
    name = 'null'
    null_values = utilities.NULL_VALUES

    def cast_default(self, value):
        """Return null if `value` can be cast as type `self.py`"""

        if isinstance(value, self.py):
            return True

        else:

            value = value.strip().lower()
            if value in self.null_values:
                return True

            return False


class ArrayType(JTSType):

    py = list
    name = 'array'

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        if isinstance(value, self.py):
            return True

        try:
            value = json.loads(value)

            if isinstance(value, self.py):
                return True

            else:
                return False

        except (TypeError, ValueError):
            return False


class ObjectType(JTSType):

    py = dict
    name = 'object'

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        if isinstance(value, self.py):
            return True

        try:
            value = json.loads(value)
            if isinstance(value, self.py):
                return True

            else:
                return False

        except (TypeError, ValueError):
            return False


class DateType(JTSType):

    py = datetime.date
    name = 'date'
    formats = ('default', 'any', 'fmt')
    ISO8601 = '%Y-%m-%d'

    # TODO: stuff from messy tables for date parsing, to replace this simple format map?
    # https://github.com/okfn/messytables/blob/master/messytables/dateparser.py#L10
    raw_formats = ['DD/MM/YYYY', 'DD/MM/YY', 'YYYY/MM/DD']
    py_formats = ['%d/%m/%Y', '%d/%m/%y', '%Y/%m/%d']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        try:
            return datetime.datetime.strptime(value, self.ISO8601).date()

        except ValueError:
            return False

    def cast_any(self, value):

        try:
            return date_parse(value).date()

        except ValueError:
            return False

    def cast_fmt(self, value):

        _pattern = self.format.strip('fmt:')
        _format = self.format_map.get(_pattern, self.ISO8601)

        try:
            return datetime.datetime.strptime(value, _format).date()

        except ValueError:
            return False


class TimeType(JTSType):

    py = time
    name = 'time'
    formats = ('default', 'any', 'fmt')
    ISO8601 = '%H:%M:%S'

    # TODO: stuff from messy tables for date parsing, to replace this simple format map?
    # https://github.com/okfn/messytables/blob/master/messytables/dateparser.py#L10
    raw_formats = ['HH/MM/SS']
    py_formats = ['%H:%M:%S']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        try:
            return time.strptime(value, self.ISO8601)

        except ValueError:
            return False

    def cast_any(self, value):

        try:
            return date_parse(value).time()

        except ValueError:
            return False

    def cast_fmt(self, value):

        _pattern = self.format.strip('fmt:')
        _format = self.format_map.get(_pattern, self.ISO8601)

        try:
            return datetime.datetime.strptime(value, _format).date()

        except ValueError:
            return False


class DateTimeType(JTSType):

    py = datetime.datetime
    name = 'datetime'
    formats = ('default', 'any', 'fmt')
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

    # TODO: stuff from messy tables for date parsing, to replace this simple format map?
    # https://github.com/okfn/messytables/blob/master/messytables/dateparser.py#L10
    raw_formats = ['DD/MM/YYYYThh/mm/ss']
    py_formats = ['%Y/%m/%dT%H:%M:%S']
    format_map = dict(zip(raw_formats, py_formats))

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        try:
            return datetime.datetime.strptime(value, self.ISO8601)

        except ValueError:
            return False

    def cast_any(self, value):

        try:
            return date_parse(value)

        except ValueError:
            return False

    def cast_fmt(self, value):

        _pattern = self.format.strip('fmt:')
        _format = self.format_map.get(_pattern, self.ISO8601)

        try:
            return datetime.datetime.strptime(value, _format)

        except ValueError:
            return False


class GeoPointType(JTSType):

    py = compat.str, list, dict
    name = 'geopoint'
    formats = ('default', 'array', 'object')

    def cast_default(self, value):

        if self._type_check(value):
            if len(value.split(',')) == 2:
                return True
            return False

        try:
            value = json.loads(value)
            if isinstance(value, self.py):
                return True

            else:
                return False

        except (TypeError, ValueError):
            return False

        return False

    def cast_array(self, value):
        raise NotImplementedError

    def cast_object(self, value):
        raise NotImplementedError


class GeoJSONType(JTSType):

    py = dict
    name = 'geojson'
    formats = ('default', 'topojson')
    spec = {
        'types': ['Point', 'MultiPoint', 'LineString', 'MultiLineString',
                  'Polygon', 'MultiPolygon', 'GeometryCollection', 'Feature',
                  'FeatureCollection']
    }

    def cast_default(self, value):
        """Return boolean if `value` can be cast as type `self.py`"""

        if self._type_check(value):
            return True

        try:
            value = json.loads(value)
            if isinstance(value, self.py):
                return True

            else:
                return False

        except (TypeError, ValueError):
            return False


    def cast_topojson(self, value):
        raise NotImplementedError


class AnyType(JTSType):

    name = 'any'

    def cast(self, value):
        return True


def _available_types():
    """Return available types."""
    return (AnyType, StringType, BooleanType, NumberType, IntegerType, NullType,
            DateType, TimeType, DateTimeType, ArrayType, ObjectType,
            GeoPointType, GeoJSONType)


class TypeGuesser(object):

    """Guess the type for a value.

    Returns:
        * A tuple  of ('type', 'format')

    """

    def __init__(self, type_options=None):
        self._types = _available_types()
        self.type_options = type_options or {}

    def cast(self, value):
        for _type in reversed(self._types):
            result = _type(self.type_options.get(_type.name, {})).cast(value)
            if result:
                # TODO: do format guessing
                rv = (_type.name, 'default')
                break

        return rv


class TypeResolver(object):

    """Get the best matching type/format from a list of possible ones."""

    def __init__(self):
        self._types = _available_types()

    def get(self, results):

        variants = set(results)

        # only one candidate... that's easy.
        if len(variants) == 1:
            rv = {
                'type': results[0][0],
                'format': results[0][1],
            }

        else:
            counts = {}
            for result in results:
                if counts.get(result):
                    counts[result] += 1
                else:
                    counts[result] = 1

            # tuple representation of `counts` dict, sorted by values of `counts`
            sorted_counts = sorted(counts.items(), key=operator.itemgetter(1),
                                   reverse=True)
            rv = {
                'type': sorted_counts[0][0][0],
                'format': sorted_counts[0][0][1]
            }

        return rv
