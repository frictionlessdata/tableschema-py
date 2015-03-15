# JTSKit

[![Travis Build Status](https://travis-ci.org/okfn/jtskit-py.svg?branch=master)](https://travis-ci.org/okfn/jtskit-py) [![Coveralls](http://img.shields.io/coveralls/okfn/jtskit-py.svg?branch=master)](https://coveralls.io/r/okfn/jtskit-py?branch=master)

A utility library for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/) in Python.

## Goals

* A core set of utilities for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/)
* Use in *other* packages that deal with actual validation of data, or other 'higher level' use cases around JSON Table Schema (e.g.: [Tabular Validator](https://github.com/okfn/tabular-validator))
* Be 100% compliant with the the JSON Table Schema specification


## Components

* `types`: a collection of classes to validate type/format of data described by a JSON Table Schema
* `models.JSONTableSchema`: A model around a schema with useful methods for interaction
* `infer`: a utility that creates a JSON Table Schema based on a data sample
* `ensure`: a utility to validate a **schema** as valid according to the current spec

Let's look at each of these in more detail.

### Types

```
from jtskit import _types
```

Type and format checking for data values.

### Models

```
from jtskit.models import JSONTableSchema
```

A model of a schema with helpful methods for working with the data a schema represents.

### Infer

```
from jtskit import infer
```

Give a sample of data, get back a schema for the data.

### Ensure

```
from jtskit import ensure
```

Give a schema as any of JSON file, url to JSON file, or a Python dict, and get back a response as to whether it is valid.

## CLI

JTSKit features a CLI called `jtskit`. This CLI exposes the `infer` and `ensure` functions for command line use.

### Infer

```
> jtskit infer path/to/data.csv
```

The response is a schema as JSON.

### Ensure

```
> jtskit ensure path/to-schema.json
```

The response is...
