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
from tableschema import Schema, exceptions


# Constants

BASE_URL = 'https://raw.githubusercontent.com/frictionlessdata/tableschema-py/master/%s'
DESCRIPTOR_MIN = {'fields': [{'name': 'id'}, {'name': 'height', 'type': 'integer'}]}
DESCRIPTOR_MAX = {
    'fields': [
        {'name': 'id', 'type': 'string', 'constraints': {'required': True}},
        {'name': 'height', 'type': 'number'},
        {'name': 'age', 'type': 'integer'},
        {'name': 'name', 'type': 'string'},
        {'name': 'occupation', 'type': 'string'},
    ],
    'primaryKey': ['id'],
    'foreignKeys': [{'fields': ['name'], 'reference': {'resource': '', 'fields': ['id']}}],
}


# Tests


def test_init():
    assert Schema(DESCRIPTOR_MIN)
    assert Schema(DESCRIPTOR_MAX)
    assert Schema('data/schema_valid_full.json')
    assert Schema('data/schema_valid_simple.json')


def test_init_invalid():
    with pytest.raises(exceptions.SchemaValidationError) as exception:
        Schema('data/schema_invalid_multiple_errors.json')


def test_descriptor(apply_defaults):
    assert Schema(DESCRIPTOR_MIN).descriptor == apply_defaults(DESCRIPTOR_MIN)
    assert Schema(DESCRIPTOR_MAX).descriptor == apply_defaults(DESCRIPTOR_MAX)


def test_descriptor_path(apply_defaults):
    path = 'data/schema_valid_simple.json'
    actual = Schema(path).descriptor
    expect = apply_defaults(json.load(io.open(path, encoding='utf-8')))
    assert actual == expect


def test_descriptor_url(apply_defaults):
    url = BASE_URL % 'data/schema_valid_simple.json'
    actual = Schema(url).descriptor
    expect = apply_defaults(requests.get(url).json())
    assert actual == expect


def test_descriptor_applied_defaults():
    assert Schema(DESCRIPTOR_MIN).descriptor == {
        'fields': [
            {'name': 'id', 'type': 'string', 'format': 'default'},
            {'name': 'height', 'type': 'integer', 'format': 'default'},
        ],
        'missingValues': [''],
    }

def test_cast_row():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string', 'string']
    target = ['string', Decimal(10.0), 1, 'string', 'string']
    assert schema.cast_row(source) == target


def test_cast_row_null_values():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '', '-', 'string', 'null']
    target = ['string', None, None, 'string', None]
    assert schema.cast_row(source) == target


def test_cast_row_too_short():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string']
    with pytest.raises(exceptions.InvalidCastError):
        schema.cast_row(source)


def test_cast_row_too_long():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string', 'string', 'string']
    with pytest.raises(exceptions.InvalidCastError):
        schema.cast_row(source)


def test_cast_row_wrong_type_no_fail_fast_true():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '10.6', 'string', 'string']
    with pytest.raises(exceptions.MultipleInvalid):
        schema.cast_row(source, no_fail_fast=True)


def test_cast_row_wrong_type_multiple_errors():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '10.6', 'string', 'string']
    with pytest.raises(exceptions.MultipleInvalid) as excinfo:
        schema.cast_row(source, no_fail_fast=True)
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


def test_save(tmpdir, apply_defaults):
    path = str(tmpdir.join('schema.json'))
    Schema(DESCRIPTOR_MIN).save(path)
    assert json.load(io.open(path, encoding='utf-8')) == apply_defaults(DESCRIPTOR_MIN)
