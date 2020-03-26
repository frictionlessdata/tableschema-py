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
from collections import OrderedDict
from decimal import Decimal
from tableschema import Schema, FailedCast, exceptions


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
    'missingValues': ['', '-', 'null'],
}


# General


def test_init():
    assert Schema(DESCRIPTOR_MIN)
    assert Schema(DESCRIPTOR_MAX)
    assert Schema('data/schema_valid_full.json')
    assert Schema('data/schema_valid_simple.json')


def test_init_invalid_in_strict_mode():
    with pytest.raises(exceptions.TableSchemaException) as exception:
        Schema('data/schema_invalid_multiple_errors.json', strict=True)


def test_descriptor(apply_defaults):
    assert Schema(DESCRIPTOR_MIN).descriptor == apply_defaults(DESCRIPTOR_MIN)
    assert Schema(DESCRIPTOR_MAX).descriptor == apply_defaults(DESCRIPTOR_MAX)


def test_descriptor_path(apply_defaults):
    path = 'data/schema_valid_simple.json'
    actual = Schema(path).descriptor
    with io.open(path, encoding='utf-8') as file:
        expect = apply_defaults(json.load(file))
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
    with pytest.raises(exceptions.CastError):
        schema.cast_row(source)


def test_cast_row_too_long():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string', 'string', 'string']
    with pytest.raises(exceptions.CastError):
        schema.cast_row(source)


def test_cast_row_wrong_type():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '10.6', 'string', 'string']
    with pytest.raises(exceptions.CastError):
        schema.cast_row(source)


def test_cast_row_wrong_type_multiple_errors():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '10.6', 'string', 'string']
    with pytest.raises(exceptions.CastError) as excinfo:
        schema.cast_row(source)
    assert len(excinfo.value.errors) == 2



# Test row casting with exception handler i.e. don't fail immediately

def _check_error(
        error, expect_exc_class, expect_exc_str, expect_row_number=None,
        expect_row_data=None, expect_error_data=None):
    # Helper function to check all given expectations on handled errors.
    # error must be a (exc, row_number, row_data, error_data)-tuple

    # Make this a namedtuple?
    exc, row_number, row_data, error_data = error
    assert isinstance(exc, expect_exc_class)
    assert expect_exc_str in str(exc)
    if expect_row_number is not None:
        # actual row number including header line
        assert row_number == expect_row_number
    if expect_row_data is not None:
        assert row_data == expect_row_data
    if error_data is not None:
        assert error_data == expect_error_data


def test_cast_row_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string', 'string']
    target = ['string', Decimal(10.0), 1, 'string', 'string']
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    assert schema.cast_row(source, exc_handler=handler) == target
    assert len(errors) == 0


def test_cast_row_null_values_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '', '-', 'string', 'null']
    target = ['string', None, None, 'string', None]
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    assert schema.cast_row(source, exc_handler=handler) == target
    assert len(errors) == 0


def test_cast_row_too_short_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string']
    # Missing values get substituted by None
    target = ['string', Decimal(10.0), 1, 'string', None]
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    assert schema.cast_row(source, exc_handler=handler) == target
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('id', 'string'), ('height', '10.0'), ('age', '1'),
         ('name', 'string'), ('occupation', None)])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=None,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)

def test_cast_row_too_long_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', '10.0', '1', 'string', 'string', 'string']
    # superfluous values are left out
    target = ['string', Decimal(10.0), 1, 'string', 'string']
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    assert schema.cast_row(source, exc_handler=handler) == target
    assert len(errors) == 1
    # superfluous values are keyed with col num for error reporting
    expect_row_data = OrderedDict(
        [('id', 'string'), ('height', '10.0'), ('age', '1'),
         ('name', 'string'), ('occupation', 'string'),
         ('tableschema-cast-error-extra-col-6', 'string')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=None,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)


def test_cast_row_wrong_type_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '1', 'string', 'string']
    target = ['string', 'notdecimal', 1, 'string', 'string']
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = schema.cast_row(source, exc_handler=handler)
    assert actual == target
    assert isinstance(actual[1], FailedCast)
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('id', 'string'), ('height', 'notdecimal'), ('age', '1'),
         ('name', 'string'), ('occupation', 'string')])
    expect_error_data = OrderedDict([('height', 'notdecimal')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='There are 1 cast errors', expect_row_number=None,
        expect_row_data=expect_row_data, expect_error_data=expect_error_data)
    exc = errors[0][0]
    assert len(exc.errors) == 1


def test_cast_row_wrong_type_multiple_errors_handled():
    schema = Schema(DESCRIPTOR_MAX)
    source = ['string', 'notdecimal', '10.6', 'string', 'string']
    target = ['string', 'notdecimal', '10.6', 'string', 'string']
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = schema.cast_row(source, exc_handler=handler)
    assert actual == target
    assert isinstance(actual[1], FailedCast)
    assert isinstance(actual[2], FailedCast)
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('id', 'string'), ('height', 'notdecimal'), ('age', '10.6'),
         ('name', 'string'), ('occupation', 'string')])
    expect_error_data = OrderedDict(
        [('height', 'notdecimal'),('age', '10.6')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='There are 2 cast errors', expect_row_number=None,
        expect_row_data=expect_row_data, expect_error_data=expect_error_data)
    exc = errors[0][0]
    assert len(exc.errors) == 2


def test_fields():
    expect = ['id', 'height']
    actual = [field.name for field in Schema(DESCRIPTOR_MIN).fields]
    assert expect == actual


def test_get_field():
    schema = Schema(DESCRIPTOR_MIN)
    assert schema.get_field('id').name == 'id'
    assert schema.get_field('height').name == 'height'
    assert schema.get_field('undefined') is None


def test_update_field():
    schema = Schema(DESCRIPTOR_MIN)
    assert schema.update_field('id', {'type': 'number'}) is True
    assert schema.update_field('height', {'type': 'number'}) is True
    assert schema.update_field('unknown', {'type': 'number'}) is False
    schema.commit()
    assert schema.get_field('id').type == 'number'
    assert schema.get_field('height').type == 'number'


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
    with io.open(path, encoding='utf-8') as file:
        descriptor = json.load(file)
    assert descriptor == apply_defaults(DESCRIPTOR_MIN)


def test_infer():
    data = [
      ['id', 'age', 'name'],
      ['1','39','Paul'],
      ['2','23','Jimmy'],
      ['3','36','Jane'],
      ['4','N/A','Judy'],
    ]
    schema = Schema()
    schema.infer(data)
    assert schema.descriptor == {
        'fields': [
            {'format': 'default', 'name': 'id', 'type': 'integer'},
            {'format': 'default', 'name': 'age', 'type': 'integer'},
            {'format': 'default', 'name': 'name', 'type': 'string'}],
        'missingValues': ['']}
    data = [
      ['id', 'age', 'name'],
      ['1','39','Paul'],
      ['2','23','Jimmy'],
      ['3','36','Jane'],
      ['4','N/A','Judy'],
    ]
    schema = Schema()
    schema.infer(data, confidence=0.8)
    assert schema.descriptor == {
        'fields': [
            {'format': 'default', 'name': 'id', 'type': 'integer'},
            {'format': 'default', 'name': 'age', 'type': 'string'},
            {'format': 'default', 'name': 'name', 'type': 'string'}],
        'missingValues': ['']}

    class AllStrings():
        def cast(self, value):
            return [('string', 'default', 0)]
    data = [
      ['id', 'age', 'name'],
      ['1','39','Paul'],
      ['2','23','Jimmy'],
      ['3','36','Jane'],
      ['4','100','Judy'],
    ]

    schema = Schema()
    schema.infer(data, confidence=0.8, guesser_cls=AllStrings)
    assert schema.descriptor['fields'] == [
            {'format': 'default', 'name': 'id', 'type': 'string'},
            {'format': 'default', 'name': 'age', 'type': 'string'},
            {'format': 'default', 'name': 'name', 'type': 'string'}]
    assert schema.descriptor == {
        'fields': [
            {'format': 'default', 'name': 'id', 'type': 'string'},
            {'format': 'default', 'name': 'age', 'type': 'string'},
            {'format': 'default', 'name': 'name', 'type': 'string'}],
        'missingValues': ['']}


def test_add_remove_field():
    schema = Schema()
    schema.add_field({'name': 'name'})
    field = schema.remove_field('name')
    assert field.name == 'name'


def test_primary_foreign_keys_as_array():
    descriptor = {
        'fields': [{'name': 'name'}],
        'primaryKey': ['name'],
        'foreignKeys': [{
            'fields': ['parent_id'],
            'reference': {'resource': 'resource', 'fields': ['id']}
        }]
    }
    schema = Schema(descriptor)
    assert schema.primary_key == ['name']
    assert schema.foreign_keys == [{
        'fields': ['parent_id'],
        'reference': {'resource': 'resource', 'fields': ['id']}
    }]


def test_primary_foreign_keys_as_string():
    descriptor = {
        'fields': [{'name': 'name'}],
        'primaryKey': 'name',
        'foreignKeys': [{
            'fields': 'parent_id',
            'reference': {'resource': 'resource', 'fields': 'id'}
        }]
    }
    schema = Schema(descriptor)
    assert schema.primary_key == ['name']
    assert schema.foreign_keys == [{
        'fields': ['parent_id'],
        'reference': {'resource': 'resource', 'fields': ['id']}
    }]


def test_fields_have_public_backreference_to_schema():
    schema = Schema('data/schema_valid_full.json')
    assert schema.get_field('first_name').schema == schema
    assert schema.get_field('last_name').schema == schema


# Issues


def test_schema_field_date_format_issue_177():
    descriptor = {'fields':[{'name':'myfield', 'type':'date', 'format':'%d/%m/%y'}]}
    schema = Schema(descriptor)
    assert schema


def test_schema_field_time_format_issue_177():
    descriptor = {'fields':[{'name':'myfield', 'type':'time', 'format':'%H:%M:%S'}]}
    schema = Schema(descriptor)
    assert schema


def test_schema_add_remove_field_issue_218():
    descriptor = {
        'fields':  [
            {'name': 'test_1', 'type': 'string', 'format': 'default'},
            {'name': 'test_2', 'type': 'string', 'format': 'default'},
            {'name': 'test_3', 'type': 'string', 'format': 'default'},
        ]
    }
    test_schema = Schema(descriptor)
    test_schema.remove_field('test_1')
    test_schema.add_field({'name': 'test_4', 'type': 'string', 'format': 'default'})
