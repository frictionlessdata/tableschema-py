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
* Use in *other* packages that deal with actual validation of data, or other 'higher level' use cases around JSON Table Schema (e.g.: [Tabular Validator](https://github.com/okfn/tabular-validator))
* Be 100% compliant with the the JSON Table Schema specification (we are not there yet)


### Components

* `types`: a collection of classes to validate type/format of data described by a JSON Table Schema
* `model.JSONTableSchema`: A model around a schema with useful methods for interaction
* `infer`: a utility that creates a JSON Table Schema based on a data sample
* `validate`: a utility to validate a **schema** as valid according to the current spec

Let's look at each of these in more detail.

#### Types

```
from jsontableschema import types
```

Type and format checking for data values.

#### Model

```
from jsontableschema.model import JSONTableSchema
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
