# JSON Table Schema

[![Travis](https://travis-ci.org/frictionlessdata/jsontableschema-py.svg?branch=master)](https://travis-ci.org/frictionlessdata/jsontableschema-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/jsontableschema-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/jsontableschema-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/jsontableschema.svg)](https://pypi.python.org/pypi/jsontableschema)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A utility library for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/) in Python.

## Features

- `Table` to work with data tables described by JSON Table Schema
- `Schema` representing JSON Table Schema
- `Field` representing JSON Table Schema field
- `Storage` to connect your tables to different storage backends like SQL Database
- `validate` to validate JSON Table Schema
- `infer` to infer JSON Table Schema from data

## Gettings Started

### Installation

```bash
pip install jsontableschema
```
> This package follow SemVer versioning

## Example

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

## Documentation

Let's look at each of the components in more detail.

### Table

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

### Storage

On level between the high-level interface and low-level driver package uses **Tabular Storage** concept:

![Tabular Storage](files/storage.png)

To write you own storage driver implement `jsontableschema.Storage` interface.

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

```csv
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

### exceptions

The library provides various of exceptions. Please consult with docstrings.

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

### CLI

> CLI is not a part of SemVer versionning. If you use it programatically
please pin concrete `goodtables` version to your requirements file.

JSON Table Schema features a CLI called `jsontableschema`. This CLI exposes the `infer` and `validate` functions for command line use.

Example of `validate` usage:

```
$ jsontableschema validate path/to-schema.json
```

Example of `infer` usage:

```
$ jsontableschema infer path/to/data.csv
```

The optional argument `--encoding` allows a character encoding to be specified for the data file. The default is utf-8.

The response is a schema as JSON.

## Read more

- [Docstrings](https://github.com/frictionlessdata/jsontableschema-py/tree/master/jsontableschema)
- [Changelog](https://github.com/frictionlessdata/jsontableschema-py/releases)
- [Contribute](CONTRIBUTING.md)

Thanks!
