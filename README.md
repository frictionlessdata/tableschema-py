# JTSKIT

A utility library for working with JSON Table Schema in Python.

## Goals

* A core set of utilities for working with [JSON Table Schema](http://dataprotocols.org/json-table-schema/)
* Use in *other* packages that deal with actual validation of data, or other 'higher level' use cases around JSON Table Schema (e.g.: [Tabular Validator](https://github.com/okfn/tabular-validator))
* Be 100% compliant with the the JSON Table Schema specification

## Utilities

* `types`: a collection of classes to validation type/format of data described by a JSON Table Schema
* `models.JSONTableSchema`: A model around a schema with useful methods to interact with the schema (Provides a model around a schema)
* `make`: a utility to create a JSON Table Schema based on a data sample
* `validate`: a utility to validate a **schema** as valid according to the current spec

## Status

* `types` are useful but currently incomplete (they don't deal woth format yet)
* `models.JSONTableSchema` is close to feature complete
* `make` is incomplete
* `validate` is close to feature complete, but needs a good refactor
