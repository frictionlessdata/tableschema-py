# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import warnings
import unicodecsv as csv
from tabulator import Stream
from importlib import import_module
from .model import SchemaModel
from . import compat
from . import helpers


# Module API

def push_resource(table, schema, data, backend, **backend_options):
    """Push JSONTableSchema resource to storage's table.

    All parameters should be used as keyword arguments.

    Parameters
    ----------
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.
    backend: str
        Backend name like `sql` or `bigquery`.
    backend_options: dict
        Backend options mentioned in backend docs.

    """

    # DEPRECATED [v0.7-v1)
    message = 'Function push_resource is deprecated [v0.7-v1)'
    warnings.warn(message, UserWarning)

    # Get storage
    plugin = import_module('jsontableschema.plugins.%s' % backend)
    storage = plugin.Storage(**backend_options)

    # Create table
    model = SchemaModel(schema)
    schema = model.as_python
    if storage.check(table):
        storage.delete(table)
    storage.create(table, schema)

    # Write data
    with Stream(data, with_headers=True) as stream:
        storage.write(table, stream)


def pull_resource(table, schema, data, backend, **backend_options):
    """Pull JSONTableSchema resource from storage's table.

    All parameters should be used as keyword arguments.

    Parameters
    ----------
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.
    backend: str
        Backend name like `sql` or `bigquery`.
    backend_options: dict
        Backend options mentioned in backend docs.

    """

    # DEPRECATED [v0.7-v1)
    message = 'Function pull_resource is deprecated [v0.7-v1)'
    warnings.warn(message, UserWarning)

    # Get storage
    plugin = import_module('jsontableschema.plugins.%s' % backend)
    storage = plugin.Storage(**backend_options)

    # Save schema
    mode = 'w'
    encoding = 'utf-8'
    if compat.is_py2:
        mode = 'wb'
        encoding = None
    helpers.ensure_dir(schema)
    with io.open(schema, mode=mode, encoding=encoding) as file:
        schema = storage.describe(table)
        json.dump(schema, file, indent=4)

    # Save data
    helpers.ensure_dir(data)
    with io.open(data, 'wb') as file:
        model = SchemaModel(schema)
        data = storage.read(table)
        writer = csv.writer(file, encoding='utf-8')
        writer.writerow(model.headers)
        for row in data:
            writer.writerow(row)
