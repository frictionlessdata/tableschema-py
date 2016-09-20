# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from mock import Mock, patch
from jsontableschema import Schema, Table


# Constants

BASE_URL = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/%s'
DATA_MIN = [('key', 'value'), ('one', '1'), ('two', '2')]
SCHEMA_MIN = {'fields': [{'name': 'key'}, {'name': 'value', 'type': 'integer'}]}
SCHEMA_CSV = {
    'fields': [
        {'name': 'id', 'type': 'integer', 'format': 'default', 'description': '', 'title': ''},
        {'name': 'age', 'type': 'integer', 'format': 'default', 'description': '', 'title': ''},
        {'name': 'name', 'type': 'string', 'format': 'default', 'description': '', 'title': ''},
    ],
}


# Tests

def test_schema():
    assert Table(DATA_MIN, schema=SCHEMA_MIN).schema.descriptor == SCHEMA_MIN


def test_schema_infer_tabulator():
    assert Table('data/data_infer.csv').schema.descriptor == SCHEMA_CSV


@patch('jsontableschema.table.import_module')
def test_schema_infer_storage(import_module):
    # Mocks
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe = Mock(return_value=SCHEMA_MIN),
        iter = Mock(return_value=DATA_MIN[1:]),
    )))
    assert Table('table', backend='storage').schema.descriptor == SCHEMA_MIN


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


@patch('jsontableschema.table.import_module')
def test_read_storage(import_module):
    # Mocks
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe = Mock(return_value=SCHEMA_MIN),
        iter = Mock(return_value=DATA_MIN[1:]),
    )))
    # Tests
    table = Table('table', backend='storage')
    expect = [['one', 1], ['two', 2]]
    actual = table.read()
    assert actual == expect


def test_processors():
    # Processor
    def skip_under_30(erows):
        for number, headers, row in erows:
            krow = dict(zip(headers, row))
            if krow['age'] >= 30:
                yield (number, headers, row)
    # Create table
    table = Table('data/data_infer.csv', post_cast=[skip_under_30])
    # Test stream
    table.stream.open()
    expect = [
        ['1', '39', 'Paul'],
        ['2', '23', 'Jimmy'],
        ['3', '36', 'Jane'],
        ['4', '28', 'Judy']]
    actual = table.stream.read()
    assert actual == expect
    # Test table
    expect = [
        [1, 39, 'Paul'],
        [3, 36, 'Jane']]
    actual = table.read()
    assert actual == expect
