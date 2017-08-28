# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from copy import deepcopy
from mock import Mock, patch
from tableschema import Schema, Table, exceptions


# General

BASE_URL = 'https://raw.githubusercontent.com/frictionlessdata/tableschema-py/master/%s'
DATA_MIN = [('key', 'value'), ('one', '1'), ('two', '2')]
SCHEMA_MIN = {'fields': [{'name': 'key'}, {'name': 'value', 'type': 'integer'}]}
SCHEMA_CSV = {
    'fields': [
        {'name': 'id', 'type': 'integer', 'format': 'default'},
        {'name': 'age', 'type': 'integer', 'format': 'default'},
        {'name': 'name', 'type': 'string', 'format': 'default'},
    ],
    'missingValues': [''],
}


def test_schema(apply_defaults):
    actual = Table(DATA_MIN, schema=SCHEMA_MIN).schema.descriptor
    expect = apply_defaults(SCHEMA_MIN)
    assert actual == expect


def test_schema_infer_tabulator():
    table = Table('data/data_infer.csv')
    table.infer()
    assert table.headers == ['id', 'age', 'name']
    assert table.schema.descriptor == SCHEMA_CSV


@patch('tableschema.table.import_module')
def test_schema_infer_storage(import_module, apply_defaults):
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe = Mock(return_value=SCHEMA_MIN),
        iter = Mock(return_value=DATA_MIN[1:]),
    )))
    table = Table('table', storage='storage')
    table.infer()
    assert table.headers == ['key', 'value']
    assert table.schema.descriptor == apply_defaults(SCHEMA_MIN)


def test_iter():
    table = Table(DATA_MIN, schema=SCHEMA_MIN)
    expect = [['one', 1], ['two', 2]]
    actual = list(table.iter())


def test_iter_csv():
    table = Table('data/data_infer.csv', schema=SCHEMA_CSV)
    expect = [[1, 39, 'Paul'], [2, 23, 'Jimmy'], [3, 36, 'Jane'], [4, 28, 'Judy']]
    actual = list(table.iter())
    assert actual == expect


def test_iter_web_csv():
    table = Table(BASE_URL % 'data/data_infer.csv', schema=SCHEMA_CSV)
    expect = [[1, 39, 'Paul'], [2, 23, 'Jimmy'], [3, 36, 'Jane'], [4, 28, 'Judy']]
    actual = list(table.iter())
    assert actual == expect


def test_iter_keyed():
    table = Table(DATA_MIN, schema=SCHEMA_MIN)
    expect = [{'key': 'one', 'value': 1}, {'key': 'two', 'value': 2}]
    actual = list(table.iter(keyed=True))
    assert actual == expect


def test_read_keyed():
    table = Table(DATA_MIN, schema=SCHEMA_MIN)
    expect = [{'key': 'one', 'value': 1}, {'key': 'two', 'value': 2}]
    actual = table.read(keyed=True)
    assert actual == expect


def test_read_limit():
    table = Table(DATA_MIN, schema=SCHEMA_MIN)
    expect = [['one', 1]]
    actual = table.read(limit=1)
    assert actual == expect


@patch('tableschema.table.import_module')
def test_read_storage(import_module):
    # Mocks
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe = Mock(return_value=SCHEMA_MIN),
        iter = Mock(return_value=DATA_MIN[1:]),
    )))
    # Tests
    table = Table('table', storage='storage')
    table.infer()
    expect = [['one', 1], ['two', 2]]
    actual = table.read()
    assert actual == expect


def test_processors():
    # Processor
    def skip_under_30(erows):
        for row_number, headers, row in erows:
            krow = dict(zip(headers, row))
            if krow['age'] >= 30:
                yield (row_number, headers, row)
    # Create table
    table = Table('data/data_infer.csv', post_cast=[skip_under_30])
    table.infer()
    expect = [
        [1, 39, 'Paul'],
        [3, 36, 'Jane']]
    actual = table.read()
    assert actual == expect


def test_unique_constraint_violation():
    schema = deepcopy(SCHEMA_CSV)
    schema['fields'][0]['constraints'] = {'unique': True}
    source = [
        ['id', 'age', 'name'],
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
    ]
    table = Table(source, schema=schema)
    with pytest.raises(exceptions.TableSchemaException) as excinfo:
        table.read()
    assert 'duplicates' in str(excinfo.value)


def test_unique_primary_key_violation():
    schema = deepcopy(SCHEMA_CSV)
    schema['primaryKey'] = 'id'
    source = [
        ['id', 'age', 'name'],
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
    ]
    table = Table(source, schema=schema)
    with pytest.raises(exceptions.TableSchemaException) as excinfo:
        table.read()
    assert 'duplicates' in str(excinfo.value)


def test_read_with_headers_field_names_missmathc():
    source = [
        ['id', 'bad', 'name'],
        [1, 39, 'Paul'],
    ]
    table = Table(source, schema=SCHEMA_CSV)
    with pytest.raises(exceptions.CheckError) as excinfo:
        table.read()
    assert 'match schema field names' in str(excinfo.value)


# Foreign keys

FK_SOURCE = [
  ['id', 'name', 'surname'],
  ['1', 'Alex', 'Martin'],
  ['2', 'John', 'Dockins'],
  ['3', 'Walter', 'White'],
]
FK_SCHEMA = {
  'fields': [
    {'name': 'id'},
    {'name': 'name'},
    {'name': 'surname'},
  ],
  'foreignKeys': [
    {
      'fields': 'name',
      'reference': {'resource': 'people', 'fields': 'firstname'},
    },
  ]
}
FK_REFERENCES = {
  'people': [
    {'firstname': 'Alex', 'surname': 'Martin'},
    {'firstname': 'John', 'surname': 'Dockins'},
    {'firstname': 'Walter', 'surname': 'White'},
  ]
}


def test_single_field_foreign_key():
    table = Table(FK_SOURCE, schema=FK_SCHEMA, references=FK_REFERENCES)
    rows = table.read()
    assert len(rows) == 3


def test_single_field_foreign_key_invalid():
    references = deepcopy(FK_REFERENCES)
    references['people'][2]['firstname'] = 'Max'
    table = Table(FK_SOURCE, schema=FK_SCHEMA, references=references)
    with pytest.raises(exceptions.CheckError) as excinfo:
        table.read()
    assert 'Foreign key' in str(excinfo.value)


def test_multi_field_foreign_key():
    schema = deepcopy(FK_SCHEMA)
    schema['foreignKeys'][0]['fields'] = ['name', 'surname']
    schema['foreignKeys'][0]['reference']['fields'] = ['firstname', 'surname']
    table = Table(FK_SOURCE, schema=schema, references=FK_REFERENCES)
    rows = table.read()
    assert len(rows) == 3


def test_multi_field_foreign_key_invalid():
    schema = deepcopy(FK_SCHEMA)
    schema['foreignKeys'][0]['fields'] = ['name', 'surname']
    schema['foreignKeys'][0]['reference']['fields'] = ['firstname', 'surname']
    references = deepcopy(FK_REFERENCES)
    del references['people'][2]
    table = Table(FK_SOURCE, schema=schema, references=references)
    with pytest.raises(exceptions.CheckError) as excinfo:
        table.read()
    assert 'Foreign key' in str(excinfo.value)



def test_single_field_foreign_key_with_references_function():
    references = lambda: FK_REFERENCES
    table = Table(FK_SOURCE, schema=FK_SCHEMA, references=references)
    rows = table.read()
    assert len(rows) == 3
