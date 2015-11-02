# JSON Table Schema

[![Travis Build Status](https://travis-ci.org/okfn/jsontableschema-py.svg?branch=master)](https://travis-ci.org/okfn/jsontableschema-py)
[![Coveralls](http://img.shields.io/coveralls/okfn/jsontableschema-py.svg?branch=master)](https://coveralls.io/r/okfn/jsontableschema-py?branch=master)

A utility library for working with JSON Table Schema in Python.


## Start

```
pip install jsontableschema
```

## Documentation

A utility library for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/) in Python.

### Goals

* A core set of utilities for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/)
* Use in *other* packages that deal with actual validation of data, or other 'higher level' use cases around JSON Table Schema (e.g. [Tabular Validator](https://github.com/okfn/tabular-validator))
* Be 100% compliant with the the JSON Table Schema specification (we are not there yet)


### Components

* `types`: a collection of classes to validate type/format of data described by a JSON Table Schema
* `model.SchemaModel`: A model around a schema with useful methods for interaction
* `infer`: a utility that creates a JSON Table Schema based on a data sample
* `validate`: a utility to validate a **schema** as valid according to the current spec

Let's look at each of these in more detail.

#### Types

Data values can be cast to native Python objects with a type instance from `jsontableschema.types`. 

Types can either be instantiated directly, or returned from `SchemaModel` instances.

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

#### Model

```
from jsontableschema.model import SchemaModel
```

A model of a schema with helpful methods for working with the data a schema represents.

#### Infer

```
from jsontableschema import infer
```

Give a sample of data, get back a schema for the data.

#### Validate

```
from jsontableschema import validate
```

Give a schema as any of JSON file, url to JSON file, or a Python dict, and get back a response as to whether it is valid.

### CLI

JSON Table Schema features a CLI called `jsontableschema`. This CLI exposes the `infer` and `validate` functions for command line use.

#### Infer

```
> jsontableschema infer path/to/data.csv
```

The optional argument `--encoding` allows a character encoding to be specified for the data file. The default is utf-8.

The response is a schema as JSON. 

#### Validate

```
> jsontableschema validate path/to-schema.json
```

The response is...
