# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import unicodecsv as csv
from tabulator import topen
from jsontableschema.model import SchemaModel

from . import compat
from . import utilities


# Module API

def import_resource(storage, table, schema, data):
    """Import JSONTableSchema resource to storage's table.

    Parameters
    ----------
    storage: object
        Storage object.
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.

    """

    # Create table
    model = SchemaModel(schema)
    schema = model.as_python
    if storage.check(table):
        storage.delete(table)
    storage.create(table, schema)

    # Write data
    with topen(data, with_headers=True) as data:
        storage.write(table, data)


def export_resource(storage, table, schema, data):
    """Export JSONTableSchema resource from storage's table.

    Parameters
    ----------
    storage: object
        Storage object.
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.

    """

    # Save schema
    mode = 'w'
    encoding = 'utf-8'
    if compat.is_py2:
        mode = 'wb'
        encoding = None
    utilities.ensure_dir(schema)
    with io.open(schema, mode=mode, encoding=encoding) as file:
        schema = storage.describe(table)
        json.dump(schema, file, indent=4)

    # Save data
    utilities.ensure_dir(data)
    with io.open(data, 'wb') as file:
        model = SchemaModel(schema)
        data = storage.read(table)
        writer = csv.writer(file, encoding='utf-8')
        writer.writerow(model.headers)
        for row in data:
            writer.writerow(row)
