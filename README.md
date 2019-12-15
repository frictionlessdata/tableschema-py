# tableschema-py

[![Travis](https://travis-ci.org/frictionlessdata/tableschema-py.svg?branch=master)](https://travis-ci.org/frictionlessdata/tableschema-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tableschema-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tableschema-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tableschema.svg)](https://pypi.python.org/pypi/tableschema)
[![Github](https://img.shields.io/badge/github-master-brightgreen)](https://github.com/frictionlessdata/tableschema-py)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A Python implementation of the [Table Schema](http://specs.frictionlessdata.io/table-schema/) standard.

> Read this README on [frictionlessdata.io](https://frictionlessdata.io)

## Features

- `Table` to work with data tables described by Table Schema
- `Schema` representing Table Schema
- `Field` representing Table Schema field
- `validate` to validate Table Schema
- `infer` to infer Table Schema from data
- built-in command-line interface to validate and infer schemas
- storage/plugins system to connect tables to different storage backends like SQL Database

## Getting Started

### Installation

The package uses semantic versioning. It means that major versions  could include breaking changes. It's highly recommended to specify `tableschema` version range in your `setup/requirements` file e.g. `tableschema>=1.0,<2.0`.

```bash
$ pip install tableschema
```

## Documentation

High-level documentation and tutorials:
- [Tutorial 1](https://frictionlessdata.io)
- [Tutorial 2](https://frictionlessdata.io)

## API Reference

### `Table`
```python
Table(self, source, schema=None, strict=False, post_cast=[], storage=None, **options)
```
Table representation

__Arguments__
- __source (str/list[])__: data source one of:
    - local file (path)
    - remote file (url)
    - array of arrays representing the rows
- __schema (any)__: data schema in all forms supported by `Schema` class
- __strict (bool)__: strictness option to pass to `Schema` constructor
- __post_cast (function[])__: list of post cast processors
- __storage (None)__: storage name like `sql` or `bigquery`
- __options (dict)__: `tabulator` or storage's options

__Raises__
- `exceptions.TableSchemaException`: raises on any error


#### `table.hash`
Table's SHA256 hash if it's available.

If it's already read using e.g. `table.read`, otherwise returns `None`.
In the middle of an iteration it returns hash of already read contents

__Returns__

`str/None`: SHA256 hash


#### `table.headers`
Table's headers is available

__Returns__

`str[]`: headers


#### `table.schema`
Returns schema class instance if available

__Returns__

`Schema`: schema


#### `table.size`
Table's size in BYTES if it's available

If it's already read using e.g. `table.read`, otherwise returns `None`.
In the middle of an iteration it returns size of already read contents

__Returns__

`int/None`: size in BYTES


#### `table.iter`
```python
table.iter(self, keyed=False, extended=False, cast=True, integrity=False, relations=False, foreign_keys_values=False, exc_handler=None)
```
Iterates through the table data and emits rows cast based on table schema.

__Arguments__

- __keyed (bool)__:
    yield keyed rows in a form of `{header1: value1, header2: value2}`
    (default is false; the form of rows is `[value1, value2]`)
- __extended (bool)__:
    yield extended rows in a for of `[rowNumber, [header1, header2], [value1, value2]]`
    (default is false; the form of rows is `[value1, value2]`)
- __cast (bool)__:
    disable data casting if false
    (default is true)
- __integrity (dict)__:
    dictionary in a form of `{'size': <bytes>, 'hash': '<sha256>'}`
    to check integrity of the table when it's read completely.
    Both keys are optional.
- __relations (dict)__:
    dictionary of foreign key references in a form
    of `{resource1: [{field1: value1, field2: value2}, ...], ...}`.
    If provided, foreign key fields will checked and resolved
    to one of their references (/!\ one-to-many fk are not completely resolved).
- __foreign_keys_values (dict)__:
    three-level dictionary of foreign key references optimized
    to speed up validation process in a form of
    `{resource1: {(foreign_key_field1, foreign_key_field2): {(value1, value2): {one_keyedrow}, ... }}}`.
    If not provided but relations is true, it will be created
    before the validation process by *index_foreign_keys_values* method
- __exc_handler (func)__:
    optional custom exception handler callable.
    Can be used to defer raising errors (i.e. "fail late"), e.g.
    for data validation purposes. Must support the signature mentioned below

__Custom exception handler__


```python
def exc_handler(exc, row_number=None, row_data=None, error_data=None):
    exc(Exception):
        Deferred exception instance
    row_number(int):
        Data row number that triggers exception exc
    row_data(OrderedDict):
        Invalid data row source data
    error_data(OrderedDict):
        Data row source data field subset responsible for the error, if
        applicable (e.g. invalid primary or foreign key fields). May be
        identical to row_data.
```

__Raises__
- `exceptions.TableSchemaException`: base class of any error
- `exceptions.CastError`: data cast error
- `exceptions.IntegrityError`: integrity checking error
- `exceptions.UniqueKeyError`: unique key constraint violation
- `exceptions.UnresolvedFKError`: unresolved foreign key reference error

__Returns__

`Iterator[list]`: yields rows


#### `table.read`
```python
table.read(self, keyed=False, extended=False, cast=True, limit=None, integrity=False, relations=False, foreign_keys_values=False, exc_handler=None)
```
Read the whole table and return as array of rows

**It has the same API as `table.iter` except for:***

__Arguments__
- __limit (int)__: limit count of rows to read and return

__Returns__

`list[]`: returns rows


#### `table.infer`
```python
table.infer(self, limit=100, confidence=0.75)
```
Infer a schema for the table.

It will infer and set Table Schema to `table.schema` based on table data.

__Arguments__
- __limit (int)__: limit rows sample size
- __confidence (float)__:
    how many casting errors are allowed
    (as a ratio, between 0 and 1)

__Returns__

`dict`: Table Schema descriptor


#### `table.save`
```python
table.save(self, target, storage=None, **options)
```
https://github.com/frictionlessdata/tableschema-py#table

#### `table.index_foreign_keys_values`
```python
table.index_foreign_keys_values(self, relations)
```
Creates a three-level dictionary of foreign key references

We create them optimized to speed up validation process in a form of
`{resource1: { (foreign_key_field1, foreign_key_field2) : { (value1, value2) : {one_keyedrow}, ... }}}`.

For each foreign key of the schema it will iterate through the corresponding
`relations['resource']` to create an index (i.e. a dict) of existing values
for the foreign fields and store on keyed row for each value combination.

The optimization relies on the indexation of possible values for one foreign key
in a hashmap to later speed up resolution.

This method is public to allow creating the index once to apply it
on multiple tables charing the same schema
(typically [grouped resources in datapackage](https://github.com/frictionlessdata/datapackage-py#group))

Note 1: the second key of the output is a tuple of the foreign fields,
a proxy identifier of the foreign key

Note 2: the same relation resource can be indexed multiple times
as a schema can contain more than one Foreign Keys pointing to the same resource

__Arguments__
- __relations (dict)__:
    dict of foreign key references in a form of
    `{resource1: [{field1: value1, field2: value2}, ...], ...}`.
    It must contain all resources pointed in the foreign keys schema definition.

__Returns__

`dict`:
    returns a three-level dictionary of foreign key references
    optimized to speed up validation process in a form of
    `{resource1: {(foreign_key_field1, foreign_key_field2): {(value1, value2): {one_keyedrow}, ... }}})`


### `Schema`
```python
Schema(self, descriptor={}, strict=False)
```

#### `schema.descriptor`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.errors`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.field_names`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.fields`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.foreign_keys`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.headers`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.primary_key`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.valid`
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.get_field`
```python
schema.get_field(self, name)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.get_field`
```python
schema.get_field(self, name)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.add_field`
```python
schema.add_field(self, descriptor)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.update_field`
```python
schema.update_field(self, name, update)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.remove_field`
```python
schema.remove_field(self, name)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.cast_row`
```python
schema.cast_row(self, row, fail_fast=False, row_number=None, exc_handler=None)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.infer`
```python
schema.infer(self, rows, headers=1, confidence=0.75, guesser_cls=None, resolver_cls=None)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.commit`
```python
schema.commit(self, strict=None)
```
https://github.com/frictionlessdata/tableschema-py#schema

#### `schema.save`
```python
schema.save(self, target, ensure_ascii=True)
```
https://github.com/frictionlessdata/tableschema-py#schema

### `Field`
```python
Field(self, descriptor, missing_values=[''], schema=None)
```
Table Schema field representation.

#### `field.constraints`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.descriptor`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.format`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.name`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.required`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.schema`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.type`
https://github.com/frictionlessdata/tableschema-py#field

#### `field.cast_value`
```python
field.cast_value(self, value, constraints=True, preserve_missing_values=False)
```
https://github.com/frictionlessdata/tableschema-py#field

#### `field.test_value`
```python
field.test_value(self, value, constraints=True)
```
https://github.com/frictionlessdata/tableschema-py#field

### `Storage`
```python
Storage(self, **options)
```

#### `storage.buckets`
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.connect`
```python
storage.connect(name, **options)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.create`
```python
storage.create(self, bucket, descriptor, force=False)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.delete`
```python
storage.delete(self, bucket=None, ignore=False)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.describe`
```python
storage.describe(self, bucket, descriptor=None)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.iter`
```python
storage.iter(self, bucket)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.read`
```python
storage.read(self, bucket)
```
https://github.com/frictionlessdata/tableschema-py#storage

#### `storage.write`
```python
storage.write(self, bucket, rows)
```
https://github.com/frictionlessdata/tableschema-py#storage

### `FailedCast`
```python
FailedCast(self, value)
```
Wrap an original data field value that failed to be properly casted.

FailedCast allows for further processing/yielding values but still be able
to distinguish uncasted values on the consuming side.

Delegates attribute access and the basic rich comparison methods to the
underlying object. Supports default user-defined classes hashability i.e.
is hashable based on object identity (not based on the wrapped value).

## Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

The recommended way to get started is to create and activate a project virtual environment.
To install package and development dependencies into your active environment:

```
$ make install
```

To run tests with linting and coverage:

```bash
$ make test
```

For linting, `pylama` (configured in `pylama.ini`) is used. At this stage it's already
installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://pylama.readthedocs.io/en/latest/.

For example to sort results by error type:

```bash
$ pylama --sort <path>
```

For testing, `tox` (configured in `tox.ini`) is used.
It's already installed into your environment and could be used separately with more fine-grained control as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity.
All positional arguments and options after `--` will be passed to `py.test`:

```bash
tox -e py27 -- -v tests/<path>
```

Under the hood `tox` uses `pytest` (configured in `pytest.ini`), `coverage`
and `mock` packages. These packages are available only in tox envionments.

## Changelog

Here described only breaking and the most important changes. The full changelog and documentation for all released versions can be found in the nicely formatted [commit history](https://github.com/frictionlessdata/tableschema-py/commits/master).

#### v1.12

- Support optional custom exception handling for table.iter/read (#259)

#### v1.11

- Added `preserve_missing_values` parameter to `field.cast_value`

#### v1.10

- Added an ability to check table's integrity while reading

#### v1.9

- Implemented the `table.size` and `table.hash` properties

#### v1.8

- Added `table.index_foreign_keys_values` and improved foreign key checks performance

#### v1.7

- Added `field.schema` property

#### v1.6

- In `strict` mode raise an exception if there are problems in field construction

#### v1.5

- Allow providing custom guesser and resolver to schema infer

#### v1.4

- Added `schema.update_field` method

#### v1.3

- Support datetime with no time for date casting

#### v1.2

- Support floats like 1.0 for integer casting

#### v1.1

- Added the `confidence` parameter to `infer`

#### v1.0

- The library has been rebased on the Frictionless Data specs v1 - https://frictionlessdata.io/specs/table-schema/

