# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import pytest
from collections import OrderedDict
from copy import deepcopy
from mock import Mock, patch
from tableschema import Schema, FailedCast, Table, Storage, exceptions


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


def test_schema_instance(apply_defaults):
    schema_instance = Schema(SCHEMA_MIN)
    actual = Table(DATA_MIN, schema=schema_instance).schema.descriptor
    expect = apply_defaults(SCHEMA_MIN)
    assert actual == expect


def test_schema_descriptor(apply_defaults):
    actual = Table(DATA_MIN, schema=SCHEMA_MIN).schema.descriptor
    expect = apply_defaults(SCHEMA_MIN)
    assert actual == expect


def test_schema_infer_tabulator():
    table = Table('data/data_infer.csv')
    table.infer()
    assert table.headers == ['id', 'age', 'name']
    assert table.schema.descriptor == SCHEMA_CSV


@patch('tableschema.storage.import_module')
def test_schema_infer_storage(import_module, apply_defaults):
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe=Mock(return_value=SCHEMA_MIN),
        iter=Mock(return_value=DATA_MIN[1:]),
    )))
    table = Table('table', storage='storage')
    table.infer()
    assert table.headers == ['key', 'value']
    assert table.schema.descriptor == apply_defaults(SCHEMA_MIN)


def test_schema_infer_missing_values():
    table = Table('data/data_infer_missing_values.csv')
    table.infer(missing_values=['-'])
    schema = deepcopy(SCHEMA_CSV)
    schema['missingValues'] = ['-']
    assert table.schema.descriptor == schema
    assert table.read() == [
        [1, 39, 'Paul'],
        [None, 25, 'Test'],
        [2, 23, 'Jimmy'],
        [None, 25, 'Test'],
        [3, 36, 'Jane'],
        [None, 25, 'Test'],
        [4, 28, 'Judy']
    ]


def test_infer_schema_empty_file():
    s = Table('data/empty.csv')
    d = s.infer()
    assert d == {
        'fields': [],
        'missingValues': [''],
    }


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


def test_iter_invalid_extra_cols():
    source = [
        ['key', 'value'],
        ['one', 1, 'unexpected'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert 'Row length' in str(excinfo.value)


def test_iter_missing_cols():
    source = [
        ['key', 'value'],
        ['one', ],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert 'Row length' in str(excinfo.value)


def test_iter_unique_primary_key_violation():
    schema = deepcopy(SCHEMA_CSV)
    schema['primaryKey'] = 'id'
    source = [
        ['id', 'age', 'name'],
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
    ]
    table = Table(source, schema=schema)
    with pytest.raises(exceptions.TableSchemaException) as excinfo:
        for _ in table.iter():
            pass
    assert isinstance(excinfo.value, exceptions.UniqueKeyError)
    assert 'duplicates' in str(excinfo.value)


def test_iter_with_headers_field_names_mismatch():
    source = [
        ['id', 'bad', 'name'],
        [1, 39, 'Paul'],
    ]
    table = Table(source, schema=SCHEMA_CSV)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert 'match schema field names' in str(excinfo.value)


def test_iter_invalid_col_value():
    # Test a schema-invalid column value in one row
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert 'There are 1 cast errors' in str(excinfo.value)
    error = excinfo.value.errors[0]
    assert isinstance(error, exceptions.CastError)
    assert ('Field "value" can\'t cast value "not_an_int" for type "integer"'
            in str(error))


def test_iter_invalid_col_value_no_cast():
    # Test a schema-invalid column value in one row, without value-casting
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    actual = list(table.iter(cast=False))
    # no actual casting, no cast errors
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


@patch('tableschema.storage.import_module')
def test_read_storage(import_module):
    # Mocks
    import_module.return_value = Mock(Storage=Mock(return_value=Mock(
        describe=Mock(return_value=SCHEMA_MIN),
        iter=Mock(return_value=DATA_MIN[1:]),
    )))
    # Tests
    table = Table('table', storage='storage')
    table.infer()
    expect = [['one', 1], ['two', 2]]
    actual = table.read()
    assert actual == expect


def test_read_storage_passed_as_instance():
    # Mocks
    storage = Mock(
        describe=Mock(return_value=SCHEMA_MIN),
        iter=Mock(return_value=DATA_MIN[1:]),
        spec=Storage,
    )
    # Tests
    table = Table('table', storage=storage)
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


def test_read_with_headers_field_names_mismatch():
    source = [
        ['id', 'bad', 'name'],
        [1, 39, 'Paul'],
    ]
    table = Table(source, schema=SCHEMA_CSV)
    with pytest.raises(exceptions.CastError) as excinfo:
        table.read()
    assert 'match schema field names' in str(excinfo.value)


def test_read_invalid_col_value():
    # Test a schema-invalid column value in one row
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        actual = table.read()
    assert 'There are 1 cast errors' in str(excinfo.value)
    error = excinfo.value.errors[0]
    assert isinstance(error, exceptions.CastError)
    assert ('Field "value" can\'t cast value "not_an_int" for type "integer"'
            in str(error))


def test_read_invalid_col_value_no_cast():
    # Test a schema-invalid column value in one row, without value-casting
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    actual = table.read(cast=False)
    # no actual casting, no cast errors
    assert actual == expect


# Stats/integrity

SIZE = 63
HASH = '328adab247692a1a405e83c2625d52e366389eabf8a1824931187877e8644774'

def test_size():
    table = Table('data/data.csv')
    table.read()
    assert table.size == SIZE


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_size_compressed():
    table = Table('data/data.csv.zip')
    table.read()
    assert table.size == SIZE


def test_size_remote():
    table = Table(BASE_URL % 'data/data.csv')
    table.read()
    assert table.size == SIZE


def test_size_not_read():
    table = Table(BASE_URL % 'data/data.csv')
    assert table.size is None


def test_hash():
    table = Table('data/data.csv')
    table.read()
    assert table.hash == HASH


@pytest.mark.skipif(six.PY2, reason='Support only for Python3')
def test_hash_compressed():
    table = Table('data/data.csv.zip')
    table.read()
    assert table.hash == HASH


def test_hash_remote():
    table = Table(BASE_URL % 'data/data.csv')
    table.read()
    assert table.hash == HASH


def test_hash():
    table = Table(BASE_URL % 'data/data.csv')
    assert table.hash is None


def test_read_integrity():
    table = Table('data/data.csv')
    table.read(integrity={'size': SIZE, 'hash': HASH})
    assert True

def test_read_integrity_error():
    table = Table('data/data.csv')
    with pytest.raises(exceptions.IntegrityError) as excinfo:
        table.read(integrity={'size': SIZE + 1, 'hash': HASH + 'a'})
    assert str(SIZE) in str(excinfo.value)
    assert HASH in str(excinfo.value)


def test_read_integrity_size():
    table = Table('data/data.csv')
    table.read(integrity={'size': SIZE})
    assert True


def test_read_integrity_size_error():
    table = Table('data/data.csv')
    with pytest.raises(exceptions.IntegrityError) as excinfo:
        table.read(integrity={'size': SIZE + 1})
    assert str(SIZE) in str(excinfo.value)


def test_read_integrity_hash():
    table = Table('data/data.csv')
    table.read(integrity={'hash': HASH})
    assert True


def test_read_integrity_hash_error():
    table = Table('data/data.csv')
    with pytest.raises(exceptions.IntegrityError) as excinfo:
        table.read(integrity={'hash': HASH + 'a'})
    assert HASH in str(excinfo.value)


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
FK_RELATIONS = {
  'people': [
    {'firstname': 'Alex', 'surname': 'Martin'},
    {'firstname': 'John', 'surname': 'Dockins'},
    {'firstname': 'Walter', 'surname': 'White'},
  ]
}


def test_single_field_foreign_key():
    table = Table(FK_SOURCE, schema=FK_SCHEMA)
    rows = table.read(relations=FK_RELATIONS)
    assert rows == [
      ['1', {'firstname': 'Alex', 'surname': 'Martin'}, 'Martin'],
      ['2', {'firstname': 'John', 'surname': 'Dockins'}, 'Dockins'],
      ['3', {'firstname': 'Walter', 'surname': 'White'}, 'White'],
    ]

def test_single_field_foreign_key_invalid():
    relations = deepcopy(FK_RELATIONS)
    relations['people'][2]['firstname'] = 'Max'
    table = Table(FK_SOURCE, schema=FK_SCHEMA)
    with pytest.raises(exceptions.RelationError) as excinfo:
        table.read(relations=relations)
    assert 'Foreign key' in str(excinfo.value)


def test_multi_field_foreign_key():
    schema = deepcopy(FK_SCHEMA)
    schema['foreignKeys'][0]['fields'] = ['name', 'surname']
    schema['foreignKeys'][0]['reference']['fields'] = ['firstname', 'surname']
    table = Table(FK_SOURCE, schema=schema)
    keyed_rows = table.read(keyed=True, relations=FK_RELATIONS)
    assert keyed_rows == [
      {
          'id': '1',
          'name': {'firstname': 'Alex', 'surname': 'Martin'},
          'surname': {'firstname': 'Alex', 'surname': 'Martin'},
      },
      {
          'id': '2',
          'name': {'firstname': 'John', 'surname': 'Dockins'},
          'surname': {'firstname': 'John', 'surname': 'Dockins'},
      },
      {
          'id': '3',
          'name': {'firstname': 'Walter', 'surname': 'White'},
          'surname': {'firstname': 'Walter', 'surname': 'White'},
      },
    ]


def test_multi_field_foreign_key_invalid():
    schema = deepcopy(FK_SCHEMA)
    schema['foreignKeys'][0]['fields'] = ['name', 'surname']
    schema['foreignKeys'][0]['reference']['fields'] = ['firstname', 'surname']
    relations = deepcopy(FK_RELATIONS)
    del relations['people'][2]
    table = Table(FK_SOURCE, schema=schema)
    with pytest.raises(exceptions.RelationError) as excinfo:
        table.read(relations=relations)
    assert 'Foreign key' in str(excinfo.value)


def test_iter_single_field_foreign_key_invalid():
    relations = deepcopy(FK_RELATIONS)
    relations['people'][2]['firstname'] = 'Max'
    table = Table(FK_SOURCE, schema=FK_SCHEMA)
    with pytest.raises(exceptions.RelationError) as excinfo:
        for _ in table.iter(relations=relations):
            pass
    assert isinstance(excinfo.value, exceptions.UnresolvedFKError)
    assert 'Foreign key' in str(excinfo.value)



MULTI_FK_SOURCE = [
  ['id', 'name', 'surname'],
  ['1', 'Alex', 'Martin'],
  ['2', 'John', 'Dockins'],
  ['3', 'Walter', 'White'],
]


MULTI_FK_SCHEMA = {
  'fields': [
    {'name': 'id'},
    {'name': 'name'},
    {'name': 'surname'},
  ],
  'foreignKeys': [
    {
      'fields': 'name',
      'reference': {'resource': 'firstnames', 'fields': 'firstname'},
    },
    {
      'fields': 'surname',
      'reference': {'resource': 'surnames', 'fields': 'surname'},
    },
  ]
}


MULTI_FK_RELATIONS = {
  'firstnames': [
    {'firstname': 'Alex', 'middlename': 'F.'},
    {'firstname': 'John', 'middlename': 'G.'},
    {'firstname': 'Walter', 'middlename': 'H.'},
  ],
  'surnames': [
    {'surname': 'Martin', 'title': 'Mrs'},
    {'surname': 'Dockins', 'title': 'Mr'},
    {'surname': 'White', 'title': 'Mr'},
  ]
}


def test_multi_fk_single_field_foreign_keys():
    table = Table(MULTI_FK_SOURCE, schema=MULTI_FK_SCHEMA)
    actual = table.read(relations=MULTI_FK_RELATIONS)
    expect = [
        ['1',
         {'firstname': 'Alex', 'middlename': 'F.'},
         {'surname': 'Martin', 'title': 'Mrs'},],
        ['2',
         {'firstname': 'John', 'middlename': 'G.'},
         {'surname': 'Dockins', 'title': 'Mr'},],
        ['3',
         {'firstname': 'Walter', 'middlename': 'H.'},
         {'surname': 'White', 'title': 'Mr'},],
        ]
    assert actual == expect


# Test proper stream closing in case of exceptions.
# Must use real data files because inline (list) data parser does never close
# the stream.

def test_iter_invalid_extra_cols_stream_closed():
    table = Table('data/data_invalid_extra_cols.csv', schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    # Circumvent name mangling to get at (overly private ;-))
    # __stream attribute
    assert table._Table__stream.closed


def test_iter_missing_cols_stream_closed():
    table = Table('data/data_missing_cols.csv', schema=SCHEMA_MIN)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert table._Table__stream.closed


def test_iter_unique_primary_key_violation_stream_closed():
    schema = deepcopy(SCHEMA_CSV)
    schema['primaryKey'] = 'id'
    table = Table('data/data_unique_primary_key_violation.csv', schema=schema)
    with pytest.raises(exceptions.TableSchemaException) as excinfo:
        for _ in table.iter():
            pass
    assert table._Table__stream.closed


def test_iter_with_headers_field_names_mismatch_stream_closed():
    table = Table(
        'data/data_headers_field_names_mismatch.csv', schema=SCHEMA_CSV)
    with pytest.raises(exceptions.CastError) as excinfo:
        for _ in table.iter():
            pass
    assert table._Table__stream.closed


# Test exc_handler option i.e. don't fail immediately

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


def test_iter_invalid_extra_cols_handled():
    # Test a schema-invalid extra column in one row
    source = [
        ['key', 'value'],
        ['one', 1, 'unexpected'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = list(table.iter(exc_handler=handler))
    expect = [
        ['one', 1],
        ['two', 2],
        ]
    assert actual == expect
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('key', 'one'), ('value', 1),
         ('tableschema-cast-error-extra-col-3', 'unexpected')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)


def test_iter_missing_cols_handled():
    source = [
        ['key', 'value'],
        ['one', ],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = list(table.iter(exc_handler=handler))
    expect = [
        ['one', None],
        ['two', 2],
        ]
    assert actual == expect
    expect_row_data = OrderedDict([('key', 'one'), ('value', None)])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)


def test_iter_unique_primary_key_violation_handled():
    # Test exception handler option to switch off fail-fast data validation
    # behaviour
    schema = deepcopy(SCHEMA_CSV)
    schema['primaryKey'] = 'id'
    source = [
        ['id', 'age', 'name'],
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
    ]
    table = Table(source, schema=schema)

    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = [
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
        ]
    actual = list(table.iter(exc_handler=handler))
    assert actual == expect
    assert len(errors) == 1
    exc, row_number, row_data, error_data = errors[0]
    assert isinstance(exc, exceptions.UniqueKeyError)
    assert row_number == 3  # actual row number including header line
    assert row_data == OrderedDict([('id', 1), ('age', 36), ('name', 'Jane')])
    assert error_data == OrderedDict([('id', 1)])
    assert 'duplicates' in str(exc)


def test_iter_with_headers_field_names_mismatch_handled():
    source = [
        ['id', 'bad', 'name'],
        [1, 39, 'Paul'],
        [2, 42, 'Peter'],
    ]
    table = Table(source, schema=SCHEMA_CSV)

    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = []
    actual = list(table.iter(exc_handler=handler))
    assert actual == expect
    assert len(errors) == 2
    for i, error in enumerate(errors):
        expect_keyed_row_data = OrderedDict(zip(source[0], source[i+1]))
        exc, row_number, row_data, error_data = error
        assert isinstance(exc, exceptions.CastError)
        assert row_number == i + 2  # actual row number including header line
        assert row_data == expect_keyed_row_data
        assert error_data == expect_keyed_row_data
        assert 'match schema field names' in str(exc)


def test_iter_single_field_foreign_key_invalid_handled():
    relations = deepcopy(FK_RELATIONS)
    relations['people'][2]['firstname'] = 'Max'
    table = Table(FK_SOURCE, schema=FK_SCHEMA)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = [
        ['1', {'firstname': 'Alex', 'surname': 'Martin'}, 'Martin'],
        ['2', {'firstname': 'John', 'surname': 'Dockins'}, 'Dockins'],
        ['3', {}, 'White'],
        ]
    actual = list(table.iter(relations=relations, exc_handler=handler))
    assert actual == expect
    assert len(errors) == 1
    exc, row_number, row_data, error_data = errors[0]
    assert row_number == 4
    expect_keyed_row_data = OrderedDict(zip(FK_SOURCE[0], FK_SOURCE[3]))
    assert row_data == expect_keyed_row_data
    assert error_data == OrderedDict([('name', 'Walter')])
    assert isinstance(exc, exceptions.UnresolvedFKError)
    assert 'Foreign key' in str(exc)


def test_iter_invalid_col_value_handled():
    # Test a schema-invalid column value in one row, handled
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = list(table.iter(exc_handler=handler))
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    assert actual == expect
    assert isinstance(actual[0][1], FailedCast)
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('key', 'one'), ('value', 'not_an_int')])
    expect_error_data = OrderedDict(
        [('value', 'not_an_int')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='There are 1 cast errors', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_error_data)


def test_iter_invalid_col_value_handled_no_cast():
    # Test a schema-invalid column value in one row, without value-casting
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = list(table.iter(cast=False, exc_handler=handler))
    # no actual casting, no cast errors
    assert len(errors) == 0
    assert actual == expect


def test_read_invalid_extra_cols_handled():
    # Test a schema-invalid extra column in one row
    source = [
        ['key', 'value'],
        ['one', 1, 'unexpected'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = table.read(exc_handler=handler)
    expect = [
        ['one', 1],
        ['two', 2],
        ]
    assert actual == expect
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('key', 'one'), ('value', 1),
         ('tableschema-cast-error-extra-col-3', 'unexpected')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)


def test_read_missing_cols_handled():
    source = [
        ['key', 'value'],
        ['one', ],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = table.read(exc_handler=handler)
    expect = [
        ['one', None],
        ['two', 2],
        ]
    assert actual == expect
    expect_row_data = OrderedDict([('key', 'one'), ('value', None)])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='Row length', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_row_data)


def test_read_unique_primary_key_violation_handled():
    schema = deepcopy(SCHEMA_CSV)
    schema['primaryKey'] = 'id'
    source = [
        ['id', 'age', 'name'],
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
    ]
    table = Table(source, schema=schema)

    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = [
        [1, 39, 'Paul'],
        [1, 36, 'Jane'],
        ]
    actual = table.read(exc_handler=handler)
    assert actual == expect
    assert len(errors) == 1
    exc, row_number, row_data, error_data = errors[0]
    assert isinstance(exc, exceptions.UniqueKeyError)
    assert row_number == 3  # actual row number including header line
    assert row_data == OrderedDict([('id', 1), ('age', 36), ('name', 'Jane')])
    assert error_data == OrderedDict([('id', 1)])
    assert 'duplicates' in str(exc)


def test_read_with_headers_field_names_mismatch_handled():
    source = [
        ['id', 'bad', 'name'],
        [1, 39, 'Paul'],
        [2, 42, 'Peter'],
    ]
    table = Table(source, schema=SCHEMA_CSV)

    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = []
    actual = table.read(exc_handler=handler)
    assert actual == expect
    assert len(errors) == 2
    for i, error in enumerate(errors):
        expect_keyed_row_data = OrderedDict(zip(source[0], source[i+1]))
        exc, row_number, row_data, error_data = error
        assert isinstance(exc, exceptions.CastError)
        assert row_number == i + 2  # actual row number including header line
        assert row_data == expect_keyed_row_data
        assert error_data == expect_keyed_row_data
        assert 'match schema field names' in str(exc)


def test_read_single_field_foreign_key_invalid_handled():
    relations = deepcopy(FK_RELATIONS)
    relations['people'][2]['firstname'] = 'Max'
    table = Table(FK_SOURCE, schema=FK_SCHEMA)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))

    expect = [
        ['1', {'firstname': 'Alex', 'surname': 'Martin'}, 'Martin'],
        ['2', {'firstname': 'John', 'surname': 'Dockins'}, 'Dockins'],
        ['3', {}, 'White'],
        ]
    actual = table.read(relations=relations, exc_handler=handler)
    assert actual == expect
    assert len(errors) == 1
    exc, row_number, row_data, error_data = errors[0]
    assert row_number == 4
    expect_keyed_row_data = OrderedDict(zip(FK_SOURCE[0], FK_SOURCE[3]))
    assert row_data == expect_keyed_row_data
    assert error_data == OrderedDict([('name', 'Walter')])
    assert isinstance(exc, exceptions.UnresolvedFKError)
    assert 'Foreign key' in str(exc)


def test_read_invalid_col_value_handled():
    # Test a schema-invalid column value in one row, handled
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = table.read(exc_handler=handler)
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
        ]
    assert actual == expect
    assert isinstance(actual[0][1], FailedCast)
    assert len(errors) == 1
    expect_row_data = OrderedDict(
        [('key', 'one'), ('value', 'not_an_int')])
    expect_error_data = OrderedDict(
        [('value', 'not_an_int')])
    _check_error(
        errors[0], expect_exc_class=exceptions.CastError,
        expect_exc_str='There are 1 cast errors', expect_row_number=2,
        expect_row_data=expect_row_data, expect_error_data=expect_error_data)


def test_read_invalid_col_value_handled_no_cast():
    # Test a schema-invalid column value in one row, without value-casting
    source = [
        ['key', 'value'],
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    expect = [
        ['one', 'not_an_int'],
        ['two', 2],
    ]
    table = Table(source, schema=SCHEMA_MIN)
    errors = []
    def handler(exc, row_number, row_data, error_data):
        errors.append((exc, row_number, row_data, error_data))
    actual = table.read(cast=False, exc_handler=handler)
    # no actual casting, no cast errors
    assert len(errors) == 0
    assert actual == expect


# Issues

def test_composite_primary_key_issue_194():
    source = [
        ['id1', 'id2'],
        ['a', '1'],
        ['a', '2'],
    ]
    schema = {
        'fields': [
            {'name': 'id1'},
            {'name': 'id2'},
        ],
        'primaryKey': ['id1', 'id2']
    }
    table = Table(source, schema=schema)
    assert table.read() == source[1:]


def test_composite_primary_key_fails_unique_issue_194():
    source = [
        ['id1', 'id2'],
        ['a', '1'],
        ['a', '1'],
    ]
    schema = {
        'fields': [
            {'name': 'id1'},
            {'name': 'id2'},
        ],
        'primaryKey': ['id1', 'id2']
    }
    table = Table(source, schema=schema)
    with pytest.raises(exceptions.CastError) as excinfo:
        table.read()
    assert 'duplicates' in str(excinfo.value)

def test_multiple_foreign_keys_same_field():
    schema = deepcopy(FK_SCHEMA)
    relations = deepcopy(FK_RELATIONS)
    relations['gender'] = [
        {'firstname': 'Alex', 'gender': 'male/female'},
        {'firstname': 'John', 'gender': 'male'},
        {'firstname': 'Walter', 'gender': 'male'},
        {'firstname': 'Alice', 'gender': 'female'}
    ]
    # the main ressource now has tow foreignKeys using the same 'name' field
    schema['foreignKeys'].append({
            'fields': 'name',
            'reference': {'resource': 'gender', 'fields': 'firstname'},
          })
    table = Table(FK_SOURCE, schema=schema)
    keyed_rows = table.read(keyed=True, relations=relations)
    assert keyed_rows == [
      {
          'id': '1',
          'name': {'firstname': 'Alex', 'surname': 'Martin' ,'gender': 'male/female'},
          'surname': 'Martin'
      },
      {
          'id': '2',
          'name': {'firstname': 'John', 'surname': 'Dockins', 'gender': 'male'},
          'surname': 'Dockins'
      },
      {
          'id': '3',
          'name': {'firstname': 'Walter', 'surname': 'White', 'gender': 'male'},
          'surname': 'White'
      },
    ]


def test_multiple_foreign_keys_same_field_invalid():
    schema = deepcopy(FK_SCHEMA)
    relations = deepcopy(FK_RELATIONS)
    relations['gender'] = [
        {'firstname': 'Alex', 'gender': 'male/female'},
        {'firstname': 'Johny', 'gender': 'male'},
        {'firstname': 'Walter', 'gender': 'male'},
        {'firstname': 'Alice', 'gender': 'female'}
    ]
    # the main ressource now has tow foreignKeys using the same 'name' field
    schema['foreignKeys'].append({
            'fields': 'name',
            'reference': {'resource': 'gender', 'fields': 'firstname'},
          })
    table = Table(FK_SOURCE, schema=schema)
    with pytest.raises(exceptions.RelationError) as excinfo:
        table.read(relations=relations)
    assert 'Foreign key' in str(excinfo.value)

