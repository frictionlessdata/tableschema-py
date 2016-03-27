# Contributing

The project follows the [Open Knowledge International coding standards](https://github.com/okfn/coding-standards).

## Getting Started

Recommended way to get started is to create and activate a project virtual environment.
To install package and development dependencies into active environment:

```
$ make install
```

## Linting

To lint the project codebase:

```
$ make lint
```

Under the hood `pylint` configured in `pylintrc` is used. On this stage it's already
installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://www.pylint.org/.

For example to check only errors:

```
$ pylint -E <path>
```

## Testing

To run tests with coverage:

```
$ make test
```
Under the hood `tox` powered by `py.test` and `coverage` configured in `tox.ini` is used.
It's already installed into your environment and could be used separately with more fine-grained control
as described in documentation - https://testrun.org/tox/latest/.

For example to check subset of tests against Python 2 environment with increased verbosity.
All positional arguments and options after `--` will be passed to `py.test`:

```
tox -e py27 -- -v tests/<path>
```
