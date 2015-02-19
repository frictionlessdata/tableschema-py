# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from jtskit import types
from . import base


class TestTypes(base.BaseTestCase):

    def test_string_type_simple_true(self):

        value = 'string'
        _type = types.StringType()

        self.assertTrue(_type.cast(value))

    def test_string_type_simple_false(self):

        value = 1
        _type = types.StringType()

        self.assertFalse(_type.cast(value))

    def test_integer_type_simple_true(self):

        value = 1
        _type = types.IntegerType()

        self.assertTrue(_type.cast(value))

    def test_integer_type_simple_false(self):

        value = 'string'
        _type = types.IntegerType()

        self.assertFalse(_type.cast(value))

    def test_number_type_simple_true(self):

        value = '10.00'
        _type = types.NumberType()

        self.assertTrue(_type.cast(value))

    def test_number_type_simple_false(self):

        value = 'string'
        _type = types.NumberType()

        self.assertFalse(_type.cast(value))

    def test_number_type_with_separators_true(self):

        value1 = '10,000.00'
        value2 = '10;000.00'
        _type = types.NumberType(strip_separators=True)

        self.assertTrue(_type.cast(value1))
        self.assertTrue(_type.cast(value2))

    def test_number_type_with_currencies_true(self):

        value = '$10000.00'
        _type = types.NumberType(strip_currencies=True)

        self.assertTrue(_type.cast(value))

    def test_date_type_simple_true(self):

        value = '2019-01-01'
        _type = types.DateType()

        self.assertTrue(_type.cast(value))

    def test_date_type_non_strict_true(self):

        value = '10th Jan 1969'
        _type = types.DateType(strict=False)

        self.assertTrue(_type.cast(value))

    def test_date_type_simple_false(self):

        value = '01-01-2019'
        _type = types.DateType()

        self.assertFalse(_type.cast(value))

    def test_time_type_simple_true(self):

        value = '06:00:00'
        _type = types.TimeType()

        self.assertTrue(_type.cast(value))

    def test_time_type_simple_false(self):

        value = '3 am'
        _type = types.TimeType()

        self.assertFalse(_type.cast(value))

    def test_datetime_type_simple_true(self):

        value = '2014-01-01T06:00:00Z'
        _type = types.DateTimeType()

        self.assertTrue(_type.cast(value))

    def test_datetime_type_non_strict_true(self):

        value = '10th Jan 1969 9 am'
        _type = types.DateTimeType(strict=False)

        self.assertTrue(_type.cast(value))

    def test_datetime_type_simple_false(self):

        value = 'Mon 1st Jan 2014 9 am'
        _type = types.DateTimeType()

        self.assertFalse(_type.cast(value))

    def test_boolean_type_simple_true(self):

        value = 'y'
        _type = types.BooleanType()

        self.assertTrue(_type.cast(value))

    def test_boolean_type_simple_false(self):

        value = '+'
        _type = types.BooleanType()

        self.assertFalse(_type.cast(value))

    def test_array_type_simple_true(self):

        value = ['1', '2']
        _type = types.ArrayType()

        self.assertTrue(_type.cast(value))

    def test_array_type_simple_false(self):

        value = 'string, string'
        _type = types.ArrayType()

        self.assertFalse(_type.cast(value))

    def test_object_type_simple_true(self):

        value = {'key': 'value'}
        _type = types.ObjectType()

        self.assertTrue(_type.cast(value))

    def test_object_type_simple_false(self):
        value = ['boo', 'ya']
        _type = types.ObjectType()

        self.assertFalse(_type.cast(value))
