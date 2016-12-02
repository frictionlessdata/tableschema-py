# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import pytest
import requests
from functools import partial
from jsontableschema import Field, exceptions


# Constants

DESCRIPTOR_MIN = {'name': 'id'}
DESCRIPTOR_MAX = {
    'name': 'id',
    'type': 'integer',
    'format': 'object',
    'constraints': {'required': True},
}


# Tests [general]

def test_descriptor():
    assert Field(DESCRIPTOR_MIN).descriptor == DESCRIPTOR_MIN


def test_name():
    assert Field(DESCRIPTOR_MIN).name == 'id'


def test_type():
    assert Field(DESCRIPTOR_MIN).type == 'string'
    assert Field(DESCRIPTOR_MAX).type == 'integer'


def test_format():
    assert Field(DESCRIPTOR_MIN).format == 'default'
    assert Field(DESCRIPTOR_MAX).format == 'object'


def test_constraints():
    assert Field(DESCRIPTOR_MIN).constraints == {}
    assert Field(DESCRIPTOR_MAX).constraints == {'required': True}


def test_required():
    assert Field(DESCRIPTOR_MIN).required == False
    assert Field(DESCRIPTOR_MAX).required == True


def test_cast_value():
    # Success
    assert Field(DESCRIPTOR_MAX).cast_value('1') == 1
    # Constraint error
    with pytest.raises(exceptions.ConstraintError):
        Field(DESCRIPTOR_MAX).cast_value('')


def test_cast_value_skip_constraints():
    assert Field(DESCRIPTOR_MIN).cast_value('', skip_constraints=True) == ''


def test_cast_value_null_case_insensitive():
    assert Field({'name': 'name', 'type': 'number'}).cast_value('Null') == None


def test_test_value():
    assert Field(DESCRIPTOR_MAX).test_value('1') == True
    assert Field(DESCRIPTOR_MAX).test_value('string') == False
    assert Field(DESCRIPTOR_MAX).test_value('') == False


def test_test_value_skip_constraints():
    assert Field(DESCRIPTOR_MIN).test_value('', skip_constraints=True) == True


def test_test_value_not_supported_constraint():
    assert Field(DESCRIPTOR_MIN).test_value('', constraint='bad') == True


# Tests [constraints]

def test_test_value_required():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'required': True}
    })
    test = partial(field.test_value, constraint='required')
    assert test('test') == True
    assert test('null') == False
    assert test('none') == False
    assert test('nil') == False
    assert test('nan') == False
    assert test('-') == False
    assert test('') == False
    assert test(None) == False


def test_test_value_pattern():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'pattern': '3.*'}
    })
    test = partial(field.test_value, constraint='pattern')
    assert test('3') == True
    assert test('321') == True
    assert test('123') == False


def test_test_value_unique():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'unique': True}
    })
    test = partial(field.test_value, constraint='unique')
    assert test(30000) == True
    assert test('bad') == False


def test_test_value_enum():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'enum': ['1', '2', '3']}
    })
    test = partial(field.test_value, constraint='enum')
    assert test('1') == True
    assert test(1) == True
    assert test('4') == False
    assert test(4) == False


def test_test_value_minimum():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'minimum': 1}
    })
    test = partial(field.test_value, constraint='minimum')
    assert test('2') == True
    assert test(2) == True
    assert test('1') == True
    assert test(1) == True
    assert test('0') == False
    assert test(0) == False


def test_test_value_maximum():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'maximum': 1}
    })
    test = partial(field.test_value, constraint='maximum')
    assert test('0') == True
    assert test(0) == True
    assert test('1') == True
    assert test(1) == True
    assert test('2') == False
    assert test(2) == False


def test_test_value_minLength():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'minLength': 1}
    })
    test = partial(field.test_value, constraint='minLength')
    assert test('ab') == True
    assert test('a') == True
    assert test('') == False


def test_test_value_maxLength():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'maxLength': 1}
    })
    test = partial(field.test_value, constraint='maxLength')
    assert test('') == True
    assert test('a') == True
    assert test('ab') == False
