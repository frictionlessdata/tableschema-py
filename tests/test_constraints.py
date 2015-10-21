# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from jsontableschema import types, exceptions
from . import base


class TestJTSTypeConstraints_Required(base.BaseTestCase):

    '''Test basic `required` constraints for JTSType'''

    def _make_field(self, constraints=None):
        field_constraints = constraints or {}
        return {
            'name': 'Name',
            'type': 'string',
            'format': 'default',
            'constraints': field_constraints
        }

    def test_constraints_empty_with_value(self):
        '''Empty constraints object, with value'''
        value = 'string'
        field = self._make_field()
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_empty_with_no_value(self):
        '''Empty constraints object, with no value (empty string)'''
        value = ''
        field = self._make_field()
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), '')

    def test_constraints_required_true_with_value(self):
        '''Required True with a value'''
        value = 'string'
        field = self._make_field({'required': True})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_true_with_no_value(self):
        '''Required True with no value (empty string) raises an exception.'''
        value = ''
        field = self._make_field({'required': True})
        _type = types.StringType(field)

        with pytest.raises(exceptions.ConstraintError) as e:
            _type.cast(value)
        self.assertEqual(e.value.msg, "The field 'Name' requires a value")

    def test_constraints_required_false_with_value(self):
        '''Required False with a value'''
        value = 'string'
        field = self._make_field({'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

    def test_constraints_required_false_with_no_value(self):
        '''Required False with no value (empty string)'''
        value = ''
        field = self._make_field({'required': False})
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)
