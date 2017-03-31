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
from tableschema import Field, exceptions


# Constants

DESCRIPTOR_MIN = {'name': 'id'}
DESCRIPTOR_MAX = {
    'name': 'id',
    'type': 'integer',
    'format': 'default',
    'constraints': {'required': True},
}


# Tests [general]

def test_descriptor(apply_defaults):
    assert Field(DESCRIPTOR_MIN).descriptor == apply_defaults(DESCRIPTOR_MIN)


def test_name():
    assert Field(DESCRIPTOR_MIN).name == 'id'


def test_type():
    assert Field(DESCRIPTOR_MIN).type == 'string'
    assert Field(DESCRIPTOR_MAX).type == 'integer'


def test_format():
    assert Field(DESCRIPTOR_MIN).format == 'default'
    assert Field(DESCRIPTOR_MAX).format == 'default'


def test_constraints():
    assert Field(DESCRIPTOR_MIN).constraints == {}
    assert Field(DESCRIPTOR_MAX).constraints == {'required': True}


def test_required():
    assert Field(DESCRIPTOR_MIN).required == False
    assert Field(DESCRIPTOR_MAX).required == True


def test_cast_value():
    assert Field(DESCRIPTOR_MAX).cast_value('1') == 1


def test_cast_value_constraint_error():
    with pytest.raises(exceptions.ConstraintError):
        Field(DESCRIPTOR_MAX).cast_value('')


def test_cast_value_constraints_false():
    assert Field(DESCRIPTOR_MIN).cast_value('', constraints=False) == None


def test_cast_value_null_with_missing_values():
    field = Field({'name': 'name', 'type': 'number'}, missing_values=['null'])
    assert field.cast_value('null') == None


def test_test_value():
    assert Field(DESCRIPTOR_MAX).test_value('1') == True
    assert Field(DESCRIPTOR_MAX).test_value('string') == False
    assert Field(DESCRIPTOR_MAX).test_value('') == False


def test_test_value_constraints_false():
    assert Field(DESCRIPTOR_MIN).test_value('', constraints=False) == True


# Tests [missingValues]

def test_string_missingValues():
    field = Field({
        'name': 'name',
        'type': 'string',
    }, missing_values=['', 'NA', 'N/A'])
    cast = field.cast_value
    assert cast('') == None
    assert cast('NA') == None
    assert cast('N/A') == None


def test_number_missingValues():
    field = Field({
        'name': 'name',
        'type': 'number',
    }, missing_values=['', 'NA', 'N/A'])
    cast = field.cast_value
    assert cast('') == None
    assert cast('NA') == None
    assert cast('N/A') == None


# Tests [constraints]

def test_test_value_required():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'required': True}
    }, missing_values=['', 'NA', 'N/A'])
    test = partial(field.test_value, constraints=['required'])
    assert test('test') == True
    assert test('null') == True
    assert test('none') == True
    assert test('nil') == True
    assert test('nan') == True
    assert test('NA') == False
    assert test('N/A') == False
    assert test('-') == True
    assert test('') == False
    assert test(None) == False


def test_test_value_pattern():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'pattern': '3.*'}
    })
    test = partial(field.test_value, constraints=['pattern'])
    assert test('3') == True
    assert test('321') == True
    assert test('123') == False


def test_test_value_unique():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'unique': True}
    })
    test = partial(field.test_value, constraints=['unique'])
    assert test(30000) == True
    assert test('bad') == False


def test_test_value_enum():
    field = Field({
        'name': 'name',
        'type': 'integer',
        'constraints': {'enum': ['1', '2', '3']}
    })
    test = partial(field.test_value, constraints=['enum'])
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
    test = partial(field.test_value, constraints=['minimum'])
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
    test = partial(field.test_value, constraints=['maximum'])
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
    test = partial(field.test_value, constraints=['minLength'])
    assert test('ab') == True
    assert test('a') == True
    # Null value passes
    assert test('') == True


def test_test_value_maxLength():
    field = Field({
        'name': 'name',
        'type': 'string',
        'constraints': {'maxLength': 1}
    })
    test = partial(field.test_value, constraints=['maxLength'])
    assert test('') == True
    assert test('a') == True
    assert test('ab') == False
