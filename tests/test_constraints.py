# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

import pytest

from jsontableschema import types, exceptions
from . import base


class ConstraintsBase(base.BaseTestCase):
    def _make_default_string_field(self, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': 'string',
            'format': 'default',
            'constraints': field_constraints
        }

    def _make_default_integer_field(self, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': 'integer',
            'format': 'default',
            'constraints': field_constraints
        }

    def _make_default_date_field(self, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': 'date',
            'format': 'default',
            'constraints': field_constraints
        }

    def _make_default_datetime_field(self, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': 'datetime',
            'format': 'default',
            'constraints': field_constraints
        }


class TestJTSTypeConstraints_Required(ConstraintsBase):

    '''Test basic `required` constraints for JTSType'''

    def test_constraints_empty_with_value(self):
        '''Empty constraints object, with value'''
        value = 'string'
        field = self._make_default_string_field()
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_empty_with_no_value(self):
        '''Empty constraints object, with no value (empty string)'''
        value = ''
        field = self._make_default_string_field()
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), '')

    def test_constraints_required_true_with_value(self):
        '''Required True with a value'''
        value = 'string'
        field = self._make_default_string_field({'required': True})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_true_with_no_value(self):
        '''Required True with no value (empty string) raises an exception.'''
        value = ''
        field = self._make_default_string_field({'required': True})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(e.value.msg, "The field 'Name' requires a value")

    def test_constraints_required_false_with_value(self):
        '''Required False with a value'''
        value = 'string'
        field = self._make_default_string_field({'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_false_with_no_value(self):
        '''Required False with no value (empty string)'''
        value = ''
        field = self._make_default_string_field({'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)


class TestJTSTypeConstraints_MinLength(ConstraintsBase):

    '''Test `minLength` constraint for StringType'''

    def test_constraints_minlength_valid_value(self):
        '''minLength with valid value'''
        value = 'string'
        field = self._make_default_string_field({'minLength': 5})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minlength_valid_value_equals(self):
        '''minLength with valid value equal to each other.'''
        value = 'string'
        field = self._make_default_string_field({'minLength': 6})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minlength_invalid_value(self):
        '''minLength with invalid value'''
        value = 'string'
        field = self._make_default_string_field({'minLength': 10})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must have a minimum length of 10")


class TestJTSTypeConstraints_MaxLength(ConstraintsBase):

    '''Test `maxLength` constraint for StringType'''

    def test_constraints_maxlength_valid_value(self):
        '''maxLength with valid value'''
        value = 'string'
        field = self._make_default_string_field({'maxLength': 7})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maxlength_valid_value_equals(self):
        '''maxLength with valid value equal to each other'''
        value = 'string'
        field = self._make_default_string_field({'maxLength': 6})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maxlength_invalid_value(self):
        '''maxLength with invalid value'''
        value = 'string'
        field = self._make_default_string_field({'maxLength': 5})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must have a maximum length of 5")


class TestIntegerTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for IntegerType'''

    def test_constraints_minimum_valid_value(self):
        value = 12
        field = self._make_default_integer_field({'minimum': 5})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minimum_valid_value_equals(self):
        value = 12
        field = self._make_default_integer_field({'minimum': 12})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minimum_invalid_value(self):
        value = 12
        field = self._make_default_integer_field({'minimum': 13})
        _type = types.IntegerType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than 13")


class TestIntegerTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for IntegerType'''

    def test_constraints_maximum_valid_value(self):
        value = 12
        field = self._make_default_integer_field({'maximum': 13})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maximum_valid_value_equals(self):
        value = 12
        field = self._make_default_integer_field({'maximum': 12})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maximum_invalid_value(self):
        value = 12
        field = self._make_default_integer_field({'maximum': 11})
        _type = types.IntegerType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than 11")


class TestDateTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for DateType'''

    def test_constraints_minimum_valid_value(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'minimum': '1978-05-28'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_minimum_valid_value_equals(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'minimum': '1978-05-29'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_minimum_invalid_value(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'minimum': '1978-05-30'})
        _type = types.DateType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than 1978-05-30")


class TestDateTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for DateType'''

    def test_constraints_maximum_valid_value(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'maximum': '1978-05-30'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_maximum_valid_value_equals(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'maximum': '1978-05-29'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_maximum_invalid_value(self):
        value = '1978-05-29'
        field = self._make_default_date_field({'maximum': '1978, 05, 28'})
        _type = types.DateType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than 1978-05-28")


class TestDateTimeTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for DateTimeType'''

    def test_constraints_minimum_valid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'minimum':
                                                  '1978-05-28T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_minimum_valid_value_equals(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'minimum':
                                                  '1978-05-29T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_minimum_invalid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'minimum':
                                                  '1978-05-30T12:30:20Z'})
        _type = types.DateTimeType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than "
                         "1978-05-30 12:30:20")


class TestDateTimeTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for DateTimeType'''

    def test_constraints_maximum_valid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'maximum':
                                                  '1978-05-30T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_maximum_valid_value_equals(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'maximum':
                                                  '1978-05-29T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_maximum_invalid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_datetime_field({'maximum':
                                                  '1978-05-28T12:30:20Z'})
        _type = types.DateTimeType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than "
                         "1978-05-28 12:30:20")
