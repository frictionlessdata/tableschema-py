# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import decimal
import datetime

import pytest

from jsontableschema import types, exceptions
from . import base


class ConstraintsBase(base.BaseTestCase):

    def _make_default_field(self, type, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': type,
            'format': 'default',
            'constraints': field_constraints
        }


class TestJTSTypeConstraints_Required(ConstraintsBase):

    '''Test basic `required` constraints for JTSType'''

    def test_constraints_empty_with_value(self):
        '''Empty constraints object, with value'''
        value = 'string'
        field = self._make_default_field(type='string')
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_empty_with_no_value(self):
        '''Empty constraints object, with no value (empty string)'''
        value = ''
        field = self._make_default_field(type='string')
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), '')

    def test_constraints_required_true_with_value(self):
        '''Required True with a value'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'required': True})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_true_with_no_value(self):
        '''Required True with no value (empty string) raises an exception.'''
        value = ''
        field = self._make_default_field(type='string',
                                         constraints={'required': True})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(e.value.msg, "The field 'Name' requires a value")

    def test_constraints_required_false_with_value(self):
        '''Required False with a value'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_false_with_no_value(self):
        '''Required False with no value (empty string)'''
        value = ''
        field = self._make_default_field(type='string',
                                         constraints={'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)


class TestJTSTypeConstraints_MinLength(ConstraintsBase):

    '''Test `minLength` constraint for StringType'''

    def test_constraints_minlength_valid_value(self):
        '''minLength with valid value'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'minLength': 5})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minlength_valid_value_equals(self):
        '''minLength with valid value equal to each other.'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'minLength': 6})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minlength_invalid_value(self):
        '''minLength with invalid value'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'minLength': 10})
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
        field = self._make_default_field(type='string',
                                         constraints={'maxLength': 7})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maxlength_valid_value_equals(self):
        '''maxLength with valid value equal to each other'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'maxLength': 6})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maxlength_invalid_value(self):
        '''maxLength with invalid value'''
        value = 'string'
        field = self._make_default_field(type='string',
                                         constraints={'maxLength': 5})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must have a maximum length of 5")


class TestIntegerTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for IntegerType'''

    def test_constraints_minimum_valid_value(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'minimum': 5})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minimum_valid_value_equals(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'minimum': 12})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_minimum_invalid_value(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'minimum': 13})
        _type = types.IntegerType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than 13")


class TestIntegerTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for IntegerType'''

    def test_constraints_maximum_valid_value(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'maximum': 13})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maximum_valid_value_equals(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'maximum': 12})
        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_maximum_invalid_value(self):
        value = 12
        field = self._make_default_field(type='integer',
                                         constraints={'maximum': 11})
        _type = types.IntegerType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than 11")


class TestDateTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for DateType'''

    def test_constraints_minimum_valid_value(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'minimum': '1978-05-28'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_minimum_valid_value_equals(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'minimum': '1978-05-29'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_minimum_invalid_value(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'minimum': '1978-05-30'})
        _type = types.DateType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than 1978-05-30")


class TestDateTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for DateType'''

    def test_constraints_maximum_valid_value(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'maximum': '1978-05-30'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_maximum_valid_value_equals(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'maximum': '1978-05-29'})
        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_maximum_invalid_value(self):
        value = '1978-05-29'
        field = self._make_default_field(type='date',
                                         constraints={'maximum':
                                                      '1978, 05, 28'})
        _type = types.DateType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than 1978-05-28")


class TestDateTimeTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for DateTimeType'''

    def test_constraints_minimum_valid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_field(type='datetime',
                                         constraints={'minimum':
                                                      '1978-05-28T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_minimum_valid_value_equals(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_field(type='datetime',
                                         constraints={'minimum':
                                                      '1978-05-29T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_minimum_invalid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_field(type='datetime',
                                         constraints={'minimum':
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
        field = self._make_default_field(type='datetime',
                                         constraints={'maximum':
                                                      '1978-05-30T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_maximum_valid_value_equals(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_field(type='datetime',
                                         constraints={'maximum':
                                                      '1978-05-29T12:30:20Z'})
        _type = types.DateTimeType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%SZ'))

    def test_constraints_maximum_invalid_value(self):
        value = '1978-05-29T12:30:20Z'
        field = self._make_default_field(type='datetime',
                                         constraints={'maximum':
                                                      '1978-05-28T12:30:20Z'})
        _type = types.DateTimeType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than "
                         "1978-05-28 12:30:20")


class TestTimeTypeConstraints_Minimum(ConstraintsBase):

    '''Test `minimum` constraint for TimeType'''

    def test_constraints_minimum_valid_value(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'minimum': '11:30:20'})
        _type = types.TimeType(field)

        struct_time = time.strptime(value, '%H:%M:%S')
        expected_time = datetime.time(struct_time.tm_hour, struct_time.tm_min,
                                      struct_time.tm_sec)
        self.assertEqual(_type.cast(value), expected_time)

    def test_constraints_minimum_valid_value_equals(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'minimum': '12:30:20'})
        _type = types.TimeType(field)

        struct_time = time.strptime(value, '%H:%M:%S')
        expected_time = datetime.time(struct_time.tm_hour, struct_time.tm_min,
                                      struct_time.tm_sec)
        self.assertEqual(_type.cast(value), expected_time)

    def test_constraints_minimum_invalid_value(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'minimum': '13:30:20'})
        _type = types.TimeType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be less than 13:30:20")


class TestTimeTypeConstraints_Maximum(ConstraintsBase):

    '''Test `maximum` constraint for TimeType'''

    def test_constraints_maximum_valid_value(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'maximum': '13:30:20'})
        _type = types.TimeType(field)

        struct_time = time.strptime(value, '%H:%M:%S')
        expected_time = datetime.time(struct_time.tm_hour, struct_time.tm_min,
                                      struct_time.tm_sec)
        self.assertEqual(_type.cast(value), expected_time)

    def test_constraints_maximum_valid_value_equals(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'maximum': '12:30:20'})
        _type = types.TimeType(field)

        struct_time = time.strptime(value, '%H:%M:%S')
        expected_time = datetime.time(struct_time.tm_hour, struct_time.tm_min,
                                      struct_time.tm_sec)
        self.assertEqual(_type.cast(value), expected_time)

    def test_constraints_maximum_invalid_value(self):
        value = '12:30:20'
        field = self._make_default_field(type='time',
                                         constraints={'maximum': '11:30:20'})
        _type = types.TimeType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The field 'Name' must not be more than 11:30:20")


class TestStringTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for StringType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = "bob"
        field = self._make_default_field(
            type='string', constraints={'enum': ['alice', 'bob', 'chuck']})

        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = "fred"
        field = self._make_default_field(
            type='string', constraints={'enum': ['alice', 'bob', 'chuck']})

        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")

    def test_constraints_enum_invalid_value_case_sensitive(self):
        '''value comparison is case sensitive'''
        value = "Bob"
        field = self._make_default_field(
            type='string', constraints={'enum': ['alice', 'bob', 'chuck']})

        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")


class TestIntegerTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for IntegerType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = 5
        field = self._make_default_field(
            type='integer', constraints={'enum': [1, 3, 5]})

        _type = types.IntegerType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = 2
        field = self._make_default_field(
            type='integer', constraints={'enum': [1, 3, 5]})

        _type = types.IntegerType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")


class TestNumberTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for NumberType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = 5
        field = self._make_default_field(
            type='number', constraints={'enum': ["1.0", "3.0", "5.0"]})

        _type = types.NumberType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = 2
        field = self._make_default_field(
            type='number', constraints={'enum': ["1.0", "3.0", "5.0"]})

        _type = types.NumberType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")


class TestBooleanTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for BooleanType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = 'true'
        field = self._make_default_field(
            type='boolean', constraints={'enum': [True, ]})

        _type = types.BooleanType(field)

        self.assertEqual(_type.cast(value), True)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = 'true'
        field = self._make_default_field(
            type='boolean', constraints={'enum': [False, ]})

        _type = types.BooleanType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")

    def test_constraints_enum_valid_value_alternate_truths(self):
        '''value is equivalent to possible values in enum array'''
        value = 'true'
        field = self._make_default_field(
            type='boolean', constraints={'enum': ['yes', 'y',
                                                  't', '1', 1]})

        _type = types.BooleanType(field)

        self.assertEqual(_type.cast(value), True)


class TestArrayTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for ArrayType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = ['first', 'second', 'third']
        field = self._make_default_field(
            type='array', constraints={'enum': [["first",
                                                 "second",
                                                 "third"],
                                                ["fred",
                                                 "alice",
                                                 "bob"], ]})

        _type = types.ArrayType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = ['first', 'second', 'third']
        field = self._make_default_field(
            type='array', constraints={'enum': [["fred",
                                                 "alice",
                                                 "bob"], ]})

        _type = types.ArrayType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")

    def test_constraints_enum_invalid_value_different_order(self):
        '''value is not in enum array. Same members in each array, but
        different order.'''
        value = ['first', 'second', 'third']
        field = self._make_default_field(
            type='array', constraints={'enum': [["first",
                                                 "third",
                                                 "second"], ]})

        _type = types.ArrayType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")


class TestObjectTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for ObjectType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = {'a': 'first', 'b': 'second', 'c': 'third'}
        field = self._make_default_field(
            type='object', constraints={'enum': [{'a': 'first',
                                                  'b': 'second',
                                                  'c': 'third'}]})

        _type = types.ObjectType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = {'a': 'first', 'b': 'second', 'c': 'third'}
        field = self._make_default_field(
            type='object', constraints={'enum': [{'a': 'fred',
                                                  'b': 'alice',
                                                  'c': 'bob'}]})

        _type = types.ObjectType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")

    def test_constraints_enum_valid_value_different_order(self):
        '''value is in enum array. Same members in each array, but different
        order.'''
        value = {'a': 'first', 'b': 'second', 'c': 'third'}
        field = self._make_default_field(
            type='object', constraints={'enum': [{'a': 'first',
                                                  'c': 'third',
                                                  'b': 'second'}], })

        _type = types.ObjectType(field)

        self.assertEqual(_type.cast(value), value)


class TestDateTypeConstraints_Enum(ConstraintsBase):

    '''Test `enum` constraint for DateType'''

    def test_constraints_enum_valid_value(self):
        '''value is in enum array'''
        value = "2015-10-22"
        field = self._make_default_field(
            type='date', constraints={'enum': ["2015-10-22"]})

        _type = types.DateType(field)

        self.assertEqual(_type.cast(value),
                         datetime.datetime.strptime(value, '%Y-%m-%d').date())

    def test_constraints_enum_invalid_value(self):
        '''value is not in enum array'''
        value = "2015-10-22"
        field = self._make_default_field(
            type='date', constraints={'enum': ["2015-10-23"]})

        _type = types.DateType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(
            e.value.msg, "The value for field 'Name' "
                         "must be in the enum array")
