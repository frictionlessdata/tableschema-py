# JSON Table Schema

[![Travis](https://travis-ci.org/frictionlessdata/jsontableschema-py.svg?branch=master)](https://travis-ci.org/frictionlessdata/jsontableschema-py)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/jsontableschema-py.svg?branch=master)](https://coveralls.io/r/frictionlessdata/jsontableschema-py?branch=master)
[![PyPi](https://img.shields.io/pypi/v/jsontableschema.svg)](https://pypi.python.org/pypi/jsontableschema)
[![Gitter](https://img.shields.io/gitter/room/frictionlessdata/chat.svg)](https://gitter.im/frictionlessdata/chat)

A utility library for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/) in Python.

## Table of Contents

- [Goals](#goals)
- [Installation](#installation)
- [Components](#components)
  - [Model](#model) - a python model of a JSON Table Schema with useful methods for interaction
  - [Types](#types) - a collection of classes to validate type/format and constraints of data described by a JSON Table Schema
  - [Infer](#infer) - a utility that creates a JSON Table Schema based on a data sample
  - [Validate](#validate) - a utility to validate a **schema** as valid according to the current spec
  - [Push/pull](#pushpull) - utilities to push and pull resources to/from storage
  - [Storage](#storage) - Tabular Storage interface declaration
- [Plugins](#plugins)
  - [BigQuery](#bigquery) - Tabular Storage implementation for BigQuery
  - [SQL](#sql) - Tabular Storage implementation for SQL
- [CLI](#cli)
  - [Infer](#infer-1) - command line interface to infer utility
  - [Validate](#validate-1) - command line interface to validate utility
- [Contributing](#contributing)

## Goals

* A core set of utilities for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/)
* Use in *other* packages that deal with actual validation of data, or other 'higher level' use cases around JSON Table Schema (e.g. [Tabular Validator](https://github.com/okfn/tabular-validator))
* Be 100% compliant with the the JSON Table Schema specification (we are not there yet)

## Installation

```
pip install jsontableschema
```

## Components

Let's look at each of the components in more detail.

### Model

A model of a schema with helpful methods for working with the schema and
supported data. SchemaModel instances can be initialized with a schema source as a filepath or url to a JSON file, or a Python dict. The schema is initially validated (see [validate](#validate) below), and will raise an exception if not a valid JSON Table Schema.

```python
from jsontableschema.model import SchemaModel
...
schema = SchemaModel(file_path_to_schema)

# convert a row
schema.convert_row('12345', 'a string', 'another field')

# convert a set of rows
schema.convert([['12345', 'a string', 'another field'],
                ['23456', 'string', 'another field']])
```

Some methods available to SchemaModel instances:

* `headers` - return an array of the schema headers (property)
* `required_headers` - return headers with the `required` constraint as an array (property)
* `fields` - return an array of the schema's fields (property)
* `primaryKey` - return the primary key field for the schema (property)
* `foreignKey` - return the foreign key property for the schema (property)
* `cast(field_name, value, index=0)` - return a value cast against a named `field_name`.
* `get_field(field_name, index=0)` - return the field object for `field_name`
* `has_field(field_name)` - return a bool if the field exists in the schema
* `get_type(field_name, index=0)` - return the type for a given `field_name`
* `get_fields_by_type(type_name)` - return all fields that match the given type
* `get_constraints(field_name, index=0)` - return the constraints object for a given `field_name`
* `convert_row(*args, fail_fast=False)` - convert the arguments given to the types of the current schema,
* `convert(rows, fail_fast=False)` - convert an iterable `rows` using the current schema of the SchemaModel instance.

Where the optional `index` argument is available, it can be used as a positional argument if the schema has multiple fields with the same name.
Where the option `fail_fast` is given, it will raise the first error it encouters, otherwise an exceptions.MultipleInvalid will be raised (if there are errors).

### Types

Data values can be cast to native Python objects with a type instance from `jsontableschema.types`.

Types can either be instantiated directly, or returned from `SchemaModel` instances instantiated with a JSON Table Schema.

Casting a value will check the value is of the expected type, is in the correct format, and complies with any constraints imposed by a schema. E.g. a date value (in ISO 8601 format) can be cast with a DateType instance:

```python
from jsontableschema import types, exceptions

# Create a DateType instance
date_type = types.DateType()

# Cast date string to date
cast_value = date_type.cast('2015-10-27')

print(type(cast_value))
# <type 'datetime.date'>

```

Values that can't be cast will raise an `InvalidCastError` exception.

Type instances can be initialized with [field descriptors](http://dataprotocols.org/json-table-schema/#field-descriptors). This allows formats and constraints to be defined:

```python

field_descriptor = {
    'name': 'Field Name',
    'type': 'date',
    'format': 'default',
    'constraints': {
        'required': True,
        'minimum': '1978-05-30'
    }
}

date_type = types.DateType(field_descriptor)
```

Casting a value that doesn't meet the constraints will raise a `ConstraintError` exception.

Note: the `unique` constraint is not currently supported.

### Infer

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

### Validate

Given a schema as JSON file, url to JSON file, or a Python dict, `validate` returns `True` for a valid JSON Table Schema, or raises an exception, `SchemaValidationError`.

```python
import io
import json

from jsontableschema import validate

filepath = 'schema_to_validate.json'

with io.open(filepath) as stream:
    schema = json.load(stream)

try:
    jsontableschema.validate(schema)
except jsontableschema.exceptions.SchemaValidationError as e:
   # handle errors

```

It may be useful to report multiple errors when validating a schema. This can be done with `validator.iter_errors()`.

```python

from jsontableschema import validator

filepath = 'schema_with_multiple_errors.json'
with io.open(filepath) as stream:
    schema = json.load(stream)
    errors = [i for i in validator.iter_errors(schema)]
```

Note: `validate()` validates whether a **schema** is a validate JSON Table Schema. It does **not** validate data against a schema.

### Push/pull

This utilities provide push and pull to/from storage possibilites
to JSON Table Schema resource (schema and data file).

This functionality requires some storage plugin installed. See
[plugins](#plugins) section for more information. Let's imagine we
have installed `jsontableschema-mystorage` (not a real name) plugin.

Then we could push and pull resources to/from the storage:

> All parameters should be used as keyword arguments.

```python
from jsontableschema import push_resource, pull_resource

# Push
push_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='mystorage, '**<mystorage_options>)

# Import
pull_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='mystorage', **<mystorage_options>)
```

Options could be a SQLAlchemy engine or a BigQuery project and dataset name etc.
Detailed desctiption you could find in a concrete plugin documentation.

See concrete exmples in [plugins](#plugins) section.

### Storage

On level between the high-level interface and low-level driver
package uses **Tabular Storage** concept:

![Tabular Storage](files/storage.png)

To write you own storage driver implement
`jsontableschema.storage.Storage` interface:

```python
from jsontableschema.storage import Storage

class CustomStorage(Storage):

    pass
```

Reference:
- [Tabular Storage](https://github.com/datapackages/jsontableschema-py/blob/feature/plugins-and-storage/jsontableschema/storage.py)

## Plugins

JSON Table Schema has a plugin system.
Any package with the name like `jsontableschema_<name>` could be imported as:

```python
from jsontableschema.plugins import <name>
```

If a plugin is not installed `ImportError` will be raised with
a message describing how to install the plugin.

Below there is a list of official supported plugins.

### BigQuery

Tabular Storage implementation for Google's BigQuery.

Installation:

```
$ pip install jsontableschema-bigquery
```

Push/pull:

> To start using Google BigQuery service:
> - Create a new project - [link](https://console.developers.google.com/home/dashboard)
> - Create a service key - [link](https://console.developers.google.com/apis/credentials)
> - Download json credentials and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

```python
import io
import os
import json
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from jsontableschema import push_resource, pull_resource

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
credentials = GoogleCredentials.get_application_default()
service = build('bigquery', 'v2', credentials=credentials)
project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']

# Push
push_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='bigquery', service=service, project=project, dataset='dataset', prefix='prefix_')

# Pull
pull_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='bigquery', service=service, project=project, dataset='dataset', prefix='prefix_')
```

Storage usage:

```python
from jsontableschema.plugins.bigquery import Storage

# Use Storage here
```

Reference:
- [Package Page](https://github.com/okfn/jsontableschema-bigquery-py)

### SQL

Tabular Storage implementation for SQL:

Installation:

```
$ pip install jsontableschema-sql
```

Push/pull:

```python
from sqlalchemy import create_engine
from jsontableschema import push_resource, pull_resource

engine = create_engine('sqlite:///:memory:')

# Push
push_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='sql', engine=engine, prefix='prefix_')

# Import
pull_resource(
    table='table_name', schema='schema_path', data='data_path',
    backend='sql', engine=engine, prefix='prefix_')
```

Storage usage:

```python
from jsontableschema.plugins.sql import Storage

# Use Storage here
```

Reference:
- [Package Page](https://github.com/okfn/jsontableschema-sql-py)

## CLI

JSON Table Schema features a CLI called `jsontableschema`. This CLI exposes the `infer` and `validate` functions for command line use.

### Infer

```
$ jsontableschema infer path/to/data.csv
```

The optional argument `--encoding` allows a character encoding to be specified for the data file. The default is utf-8.

The response is a schema as JSON.

See the above [Infer](#infer) section for details.

### Validate

```
$ jsontableschema validate path/to-schema.json
```

See the above [Validate](#validate) section for details.

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
