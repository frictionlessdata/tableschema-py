# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import json
import pytest
import requests
from decimal import Decimal
from jsontableschema import exceptions
from jsontableschema.schema import Schema


# Constants

BASE_URL = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/%s'
DESCRIPTOR_MIN = {'fields': [{'name': 'id'}, {'name': 'height'}]}
DESCRIPTOR_MAX = {
    'fields': [
        {'name': 'id', 'type': 'string', 'constraints': {'required': True}},
        {'name': 'height', 'type': 'number'},
        {'name': 'age', 'type': 'integer'},
        {'name': 'name', 'type': 'string'},
        {'name': 'occupation', 'type': 'string'},
    ],
    'primaryKey': 'id',
    'foreignKeys': [{'fields': 'name', 'reference': {'resource': 'self', 'fields': 'id'}}],
}


# Tests

def test_descriptor():
    # Dict
    assert Schema(DESCRIPTOR_MIN).descriptor == DESCRIPTOR_MIN
    assert Schema(DESCRIPTOR_MAX).descriptor == DESCRIPTOR_MAX
    # Path
    path = 'data/schema_valid_simple.json'
    expect = Schema(path).descriptor
    actual = json.load(io.open(path, encoding='utf-8'))
    assert expect == actual
    # Url
    url = BASE_URL % 'data/schema_valid_simple.json'
    expect = Schema(url).descriptor
    actual = requests.get(url).json()
    assert expect == actual


def test_validate():
    # Valid
    assert Schema(DESCRIPTOR_MIN).validate()
    assert Schema(DESCRIPTOR_MAX).validate()
    assert Schema('data/schema_valid_full.json').validate()
    assert Schema('data/schema_valid_simple.json').validate()
    # Invalid
    with pytest.raises(exceptions.MultipleInvalid) as exception:
        Schema('data/schema_invalid_multiple_errors.json').validate()
    # Invalid (fail fast)
    with pytest.raises(exceptions.InvalidSchemaError) as exception:
        Schema('data/schema_invalid_multiple_errors.json').validate(fail_fast=True)


def test_convert_row():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', '10.0', '1', 'string', 'string')
    target = ('string', Decimal(10.0), 1, 'string', 'string')
    assert schema.convert_row(source) == target


def test_convert_row_null_values():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', '', '-', 'string', 'null')
    target = ('string', None, None, 'string', None)
    assert schema.convert_row(source) == target


def test_convert_row_too_short():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', '10.0', '1', 'string')
    with pytest.raises(exceptions.ConversionError):
        schema.convert_row(source)


def test_convert_row_too_long():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', '10.0', '1', 'string', 'string', 'string')
    with pytest.raises(exceptions.ConversionError):
        schema.convert_row(source)


def test_convert_row_wrong_type_fail_fast():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', 'notdecimal', '10.6', 'string', 'string')
    with pytest.raises(exceptions.InvalidCastError):
        schema.convert_row(source, fail_fast=True)


def test_convert_row_wrong_type_multiple_errors():
    schema = Schema(DESCRIPTOR_MAX)
    source = ('string', 'notdecimal', '10.6', 'string', 'string')
    with pytest.raises(exceptions.MultipleInvalid) as excinfo:
        schema.convert_row(source)
    assert len(excinfo.value.errors) == 2


def test_fields():
    expect = ['id', 'height']
    actual = [field.name for field in Schema(DESCRIPTOR_MIN).fields]
    assert expect == actual


def test_get_field():
    schema = Schema(DESCRIPTOR_MIN)
    assert schema.get_field('id').name == 'id'
    assert schema.get_field('height').name == 'height'
    assert schema.get_field('undefined') is None


def test_has_field():
    schema = Schema(DESCRIPTOR_MIN)
    assert schema.has_field('id')
    assert schema.has_field('height')
    assert not schema.has_field('undefined')


def test_headers():
    assert Schema(DESCRIPTOR_MIN).headers == ['id', 'height']


def test_primary_key():
    assert Schema(DESCRIPTOR_MIN).primary_key == []
    assert Schema(DESCRIPTOR_MAX).primary_key == ['id']


def test_foreign_keys():
    assert Schema(DESCRIPTOR_MIN).foreign_keys == []
    assert Schema(DESCRIPTOR_MAX).foreign_keys == DESCRIPTOR_MAX['foreignKeys']


def test_save(tmpdir):
    path = str(tmpdir.join('schema.json'))
    Schema(DESCRIPTOR_MIN).save(path)
    assert DESCRIPTOR_MIN == json.load(io.open(path, encoding='utf-8'))
