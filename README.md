# tableschema-py

> Read this README with navigation and search on [frictionlessdata.io](https://frictionlessdata.io)

[![Travis](https://travis-ci.org/frictionlessdata/tableschema-py.svg?branch=master)](https://travis-ci.org/frictionlessdata/tableschema-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/tableschema-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/tableschema-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/tableschema.svg)](https://pypi.python.org/pypi/tableschema)
[![Github](https://img.shields.io/badge/github-master-brightgreen)](https://github.com/frictionlessdata/tableschema-py)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A library for working with [Table Schema](http://specs.frictionlessdata.io/table-schema/) in Python.

## Features

- `Table` to work with data tables described by Table Schema
- `Schema` representing Table Schema
- `Field` representing Table Schema field
- `validate` to validate Table Schema
- `infer` to infer Table Schema from data
- built-in command-line interface to validate and infer schemas
- storage/plugins system to connect tables to different storage backends like SQL Database

## Installation

The package uses semantic versioning. It means that major versions  could include breaking changes. It's highly recommended to specify `tableschema` version range in your `setup/requirements` file e.g. `tableschema>=1.0,<2.0`.

```bash
$ pip install tableschema
```

## Documentation

High-level documentation and tutorials:
- [Tutorial 1](https://frictionlessdata.io)
- [Tutorial 2](https://frictionlessdata.io)

## Reference


### Class `Table`

> `class Table(source, schema=None, strict=False, post_cast=[], storage=None, **options)`

Table representation

#### Arguments

**`source`** :&ensp;`Union`[`str`, `list`[]]:   

data source one of:
    - local file (path)
    - remote file (url)
    - array of arrays representing the rows

**`schema`** :&ensp;`any`
:   data schema in all forms supported by `Schema` class

**`strict`** :&ensp;`bool`
:   strictness option to pass to `Schema` constructor

**`post_cast`** :&ensp;`function`[]
:   list of post cast processors

**`storage`** :&ensp;`None`
:   storage name like `sql` or `bigquery`

**`options`** :&ensp;`dict`
:   `tabulator` or storage's options

#### Raises

`exceptions.TableSchemaException`: `raises` `any` `error` `that` `occurs` `in` `table` `creation` `process`
:   &nbsp;


#### Instance variables


##### Variable `hash`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Variable `headers`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Variable `schema`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Variable `size`

<https://github.com/frictionlessdata/tableschema-py#table>


#### Methods


##### Method `index_foreign_keys_values`


> `def index_foreign_keys_values(self, relations)`


##### Method `infer`


> `def infer(self, limit=100, confidence=0.75)`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Method `iter`


> `def iter(self, keyed=False, extended=False, cast=True, integrity=False, relations=False, foreign_keys_values=False, exc_handler=None)`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Method `read`


> `def read(self, keyed=False, extended=False, cast=True, limit=None, integrity=False, relations=False, foreign_keys_values=False, exc_handler=None)`

<https://github.com/frictionlessdata/tableschema-py#table>


##### Method `save`


> `def save(self, target, storage=None, **options)`

<https://github.com/frictionlessdata/tableschema-py#table>



### Class `Schema`

> `class Schema(descriptor=, strict=False)`

<https://github.com/frictionlessdata/tableschema-py#schema>


#### Instance variables


##### Variable `descriptor`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `errors`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `field_names`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `fields`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `foreign_keys`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `headers`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `primary_key`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Variable `valid`

<https://github.com/frictionlessdata/tableschema-py#schema>


#### Methods


##### Method `add_field`


> `def add_field(self, descriptor)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `cast_row`


> `def cast_row(self, row, fail_fast=False, row_number=None, exc_handler=None)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `commit`


> `def commit(self, strict=None)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `get_field`


> `def get_field(self, name)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `has_field`


> `def has_field(self, name)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `infer`


> `def infer(self, rows, headers=1, confidence=0.75, guesser_cls=None, resolver_cls=None)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `remove_field`


> `def remove_field(self, name)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `save`


> `def save(self, target, ensure_ascii=True)`

<https://github.com/frictionlessdata/tableschema-py#schema>


##### Method `update_field`


> `def update_field(self, name, update)`

<https://github.com/frictionlessdata/tableschema-py#schema>



### Class `Field`

> `class Field(descriptor, missing_values=[''], schema=None)`

Table Schema field representation.


<https://github.com/frictionlessdata/tableschema-py#field>


#### Instance variables


##### Variable `constraints`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `descriptor`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `format`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `name`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `required`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `schema`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Variable `type`

<https://github.com/frictionlessdata/tableschema-py#field>


#### Methods


##### Method `cast_value`


> `def cast_value(self, value, constraints=True, preserve_missing_values=False)`

<https://github.com/frictionlessdata/tableschema-py#field>


##### Method `test_value`


> `def test_value(self, value, constraints=True)`

<https://github.com/frictionlessdata/tableschema-py#field>



### Class `Storage`

> `class Storage(**options)`

<https://github.com/frictionlessdata/tableschema-py#storage>


#### Instance variables


##### Variable `buckets`

<https://github.com/frictionlessdata/tableschema-py#storage>


#### Static methods


##### `Method connect`


> `def connect(name, **options)`

<https://github.com/frictionlessdata/tableschema-py#storage>


#### Methods


##### Method `create`


> `def create(self, bucket, descriptor, force=False)`

<https://github.com/frictionlessdata/tableschema-py#storage>


##### Method `delete`


> `def delete(self, bucket=None, ignore=False)`

<https://github.com/frictionlessdata/tableschema-py#storage>


##### Method `describe`


> `def describe(self, bucket, descriptor=None)`

<https://github.com/frictionlessdata/tableschema-py#storage>


##### Method `iter`


> `def iter(self, bucket)`

<https://github.com/frictionlessdata/tableschema-py#storage>


##### Method `read`


> `def read(self, bucket)`

<https://github.com/frictionlessdata/tableschema-py#storage>


##### Method `write`


> `def write(self, bucket, rows)`

<https://github.com/frictionlessdata/tableschema-py#storage>



### Function `validate`


> `def validate(descriptor)`

<https://github.com/frictionlessdata/tableschema-py#schema>



### Function `infer`


> `def infer(source, headers=1, limit=100, confidence=0.75, **options)`

<https://github.com/frictionlessdata/tableschema-py#schema>



### Class `FailedCast`

> `class FailedCast(value)`

Wrap an original data field value that failed to be properly casted.

FailedCast allows for further processing/yielding values but still be able
to distinguish uncasted values on the consuming side.

Delegates attribute access and the basic rich comparison methods to the
underlying object. Supports default user-defined classes hashability i.e.
is hashable based on object identity (not based on the wrapped value).


#### Instance variables


##### Variable `value`



### Class `TableSchemaException`

> `class TableSchemaException(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `LoadError`

> `class LoadError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `ValidationError`

> `class ValidationError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `CastError`

> `class CastError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `IntegrityError`

> `class IntegrityError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `UniqueKeyError`

> `class UniqueKeyError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `RelationError`

> `class RelationError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `UnresolvedFKError`

> `class UnresolvedFKError(message, errors=[])`

Common base class for all non-exit exceptions.



### Class `StorageError`

> `class StorageError(message, errors=[])`

Common base class for all non-exit exceptions.

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

