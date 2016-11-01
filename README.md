# JSON Table Schema

[![Travis](https://travis-ci.org/frictionlessdata/jsontableschema-py.svg?branch=master)](https://travis-ci.org/frictionlessdata/jsontableschema-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/jsontableschema-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/jsontableschema-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/jsontableschema.svg)](https://pypi.python.org/pypi/jsontableschema)
[![SemVer](https://img.shields.io/badge/versions-SemVer-brightgreen.svg)](http://semver.org/)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A utility library for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/) in Python.

> With v0.7 renewed API has been introduced in backward-compatibility manner. Documentation for deprecated API could be found [here](https://github.com/frictionlessdata/jsontableschema-py/tree/0.6.5#json-table-schema). Deprecated API will be removed with v1 release.

## Features

- `Table` to work with data tables described by JSON Table Schema
- `Schema` representing JSON Table Schema
- `Field` representing JSON Table Schema field
- `validate` to validate JSON Table Schema
- `infer` to infer JSON Table Schema from data
- built-in command-line interface to validate and infer schemas
- storage/plugins system to connect tables to different storage backends like SQL Database

## Gettings Started

### Installation

```bash
pip install jsontableschema
```
### Example

```python
from jsontableschema import Table

# Create table
table = Table('path.csv', schema='schema.json')

# Print schema descriptor
print(table.schema.descriptor)

# Print cast rows in a dict form
for keyed_row in table.iter(keyed=True):
    print(keyed_row)
```

### Table

Table represents data described by JSON Table Schema:

```python
# pip install sqlalchemy jsontableschema-sql
import sqlalchemy as sa
from pprint import pprint
from jsontableschema import Table

# Data source
SOURCE = 'https://raw.githubusercontent.com/okfn/jsontableschema-py/master/data/data_infer.csv'

# Create SQL database
db = sa.create_engine('sqlite://')

# Data processor
def skip_under_30(erows):
    for number, headers, row in erows:
        krow = dict(zip(headers, row))
        if krow['age'] >= 30:
            yield (number, headers, row)

# Work with table
table = Table(SOURCE, post_cast=[skip_under_30])
table.schema.save('tmp/persons.json') # Save INFERRED schema
table.save('persons', backend='sql', engine=db) # Save data to SQL
table.save('tmp/persons.csv')  # Save data to DRIVE

# Check the result
pprint(Table('persons', backend='sql', engine=db).read(keyed=True))
pprint(Table('tmp/persons.csv').read(keyed=True))
# Will print (twice)
# [{'age': 39, 'id': 1, 'name': 'Paul'},
#  {'age': 36, 'id': 3, 'name': 'Jane'}]
```

### Schema

A model of a schema with helpful methods for working with the schema and supported data. Schema instances can be initialized with a schema source as a filepath or url to a JSON file, or a Python dict. The schema is initially validated (see [validate](#validate) below), and will raise an exception if not a valid JSON Table Schema.

```python
from jsontableschema import Schema

# Init schema
schema = Schema('path.json')

# Cast a row
schema.cast_row(['12345', 'a string', 'another field'])
```

Methods available to `Schema` instances:

- `descriptor` - return schema descriptor
- `fields` - an array of the schema's Field instances
- `headers` - an array of the schema headers
- `primary_key` - the primary key field for the schema as an array
- `foreignKey` - the foreign key property for the schema as an array
- `get_field(name)` - return the field object for given name
- `has_field(name)` - return a bool if the field exists in the schema
- `cast_row(row, no_fail_fast=False)` - return row cast against schema
- `save(target)` - save schema to filesystem

Where the option `no_fail_fast` is given, it will collect all errors it encouters and an exceptions.MultipleInvalid will be raised (if there are errors).

### Field

```python
from jsontableschemal import Field

# Init field
field = Field({'type': 'number'})

# Cast a value
field.cast_value('12345') # -> 12345
```

Data values can be cast to native Python objects with a Field instance. Type instances can be initialized with [field descriptors](http://dataprotocols.org/json-table-schema/#field-descriptors). This allows formats and constraints to be defined.

Casting a value will check the value is of the expected type, is in the correct format, and complies with any constraints imposed by a schema. E.g. a date value (in ISO 8601 format) can be cast with a DateType instance. Values that can't be cast will raise an `InvalidCastError` exception.

Casting a value that doesn't meet the constraints will raise a `ConstraintError` exception.

### validate

Given a schema as JSON file, url to JSON file, or a Python dict, `validate` returns `True` for a valid JSON Table Schema, or raises an exception, `SchemaValidationError`. It validates only **schema**, not data against schema!

```python
import io
import json

from jsontableschema import validate

with io.open('schema_to_validate.json') as stream:
    descriptor = json.load(stream)

try:
    jsontableschema.validate(descriptor)
except jsontableschema.exceptions.SchemaValidationError as exception:
   # handle error

```

It may be useful to report multiple errors when validating a schema. This can be done with `no_fail_fast` flag set to True.

```python
try:
    jsontableschema.validate(descriptor, no_fail_fast=True)
except jsontableschema.exceptions.MultipleInvalid as exception:
    for error in exception.errors:
        # handle error
```

### infer

Given headers and data, `infer` will return a JSON Table Schema as a Python dict based on the data values. Given the data file, data_to_infer.csv:

```
id,age,name
1,39,Paul
2,23,Jimmy
3,36,Jane
4,28,Judy
```

Call `infer` with headers and values from the datafile:

```python
import io
import csv

from jsontableschema import infer

filepath = 'data_to_infer.csv'
with io.open(filepath) as stream:
    headers = stream.readline().rstrip('\n').split(',')
    values = csv.reader(stream)

schema = infer(headers, values)
```

`schema` is now a schema dict:

```python
{u'fields': [
    {
        u'description': u'',
        u'format': u'default',
        u'name': u'id',
        u'title': u'',
        u'type': u'integer'
    },
    {
        u'description': u'',
        u'format': u'default',
        u'name': u'age',
        u'title': u'',
        u'type': u'integer'
    },
    {
        u'description': u'',
        u'format': u'default',
        u'name': u'name',
        u'title': u'',
        u'type': u'string'
    }]
}
```

The number of rows used by `infer` can be limited with the `row_limit` argument.

### CLI

> It's a provisional API excluded from SemVer. If you use it as a part of other program please pin concrete `goodtables` version to your requirements file.

JSON Table Schema features a CLI called `jsontableschema`. This CLI exposes the `infer` and `validate` functions for command line use.

Example of `validate` usage:

```
$ jsontableschema validate path/to-schema.json
```

Example of `infer` usage:

```
$ jsontableschema infer path/to/data.csv
```

The response is a schema as JSON. The optional argument `--encoding` allows a character encoding to be specified for the data file. The default is utf-8.

### Storage

The library includes interface declaration to implement tabular `Storage`:

![Storage](data/storage.png)

An implementor should follow `jsontableschema.Storage` interface to write his
own storage backend. This backend could be used with `Table` class. See `plugins`
system below to know how to integrate custom storage plugin.

### plugins

JSON Table Schema has a plugin system.  Any package with the name like `jsontableschema_<name>` could be imported as:

```python
from jsontableschema.plugins import <name>
```

If a plugin is not installed `ImportError` will be raised with a message describing how to install the plugin.

A list of officially supported plugins:
- BigQuery Storage - https://github.com/frictionlessdata/jsontableschema-bigquery-py
- Pandas Storage - https://github.com/frictionlessdata/jsontableschema-pandas-py
- SQL Storage - https://github.com/frictionlessdata/jsontableschema-sql-py

## API Reference

### Snapshot

```
Table(source, schema=None, post_cast=None, backend=None, **options)
    stream -> tabulator.Stream
    schema -> Schema
    name -> str
    iter(keyed/extended=False) -> (generator) (keyed/extended)row[]
    read(keyed/extended=False, limit=None) -> (keyed/extended)row[]
    save(target, backend=None, **options)
Schema(descriptor)
    descriptor -> dict
    fields -> Field[]
    headers -> str[]
    primary_key -> str[]
    foreign_keys -> str[]
    get_field(name) -> Field
    has_field(name) -> bool
    cast_row(row, no_fail_fast=False) -> row
    save(target)
Field(descriptor)
    descriptor -> dict
    name -> str
    type -> str
    format -> str
    constraints -> dict
    cast_value(value, skip_constraints=False) -> value
    test_value(value, skip_constraints=False, constraint=None) -> bool
validate(descriptor, no_fail_fast=False) -> bool
infer(headers, values) -> descriptor
exceptions
~cli
---
Storage(**options)
    buckets -> str[]
    create(bucket, descriptor, force=False)
    delete(bucket=None, ignore=False)
    describe(bucket, descriptor=None) -> descriptor
    iter(bucket) -> (generator) row[]
    read(bucket) -> row[]
    write(bucket, rows)
plugins
```

### Detailed

- [Docstrings](https://github.com/frictionlessdata/jsontableschema-py/tree/master/jsontableschema)
- [Changelog](https://github.com/frictionlessdata/jsontableschema-py/commits/master)

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
