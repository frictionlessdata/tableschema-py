# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import topen
from .schema import Schema
from . import exceptions
from . import compat


# Module API

class Table(object):
    """JSON Table Schema table representation.

    Args:
        source (mixed): data source
        schema (Schema/dict/str): schema instance or descriptor/path/url
        backend (None/str): backend name like `sql` or `bigquery`
        options (dict): tabulator options or backend options

    """

    # Public

    def __init__(self, source, schema=None, backend=None, **options):

        # Instantiate schema
        if isinstance(schema, (compat.str, dict)):
            schema = Schema(schema)

        # Set attributes
        self.__source = source
        self.__schema = schema
        self.__backend = backend
        self.__options = options

    @property
    def schema(self):
        """Schema: schema instance
        """
        if self.__schema is None:
            message = 'Schema infering is not supported yet'
            raise NotImplementedError(message)
        return self.__schema

    def iter(self, keyed=False):
        """Yields table rows.

        Args:
            keyed (bool): yield keyed rows

        Yields:
            mixed[]/mixed{}: row or keyed row

        """

        # Tabulator
        if self.__backend is None:
            options = {}
            options.update(extract_headers=True)
            options.update(self.__options)
            with topen(self.__source, **options) as table:
                for row in table:
                    row = self.schema.convert_row(row)
                    if keyed:
                        row = dict(zip(self.schema.headers, row))
                    yield row

        # Storage
        else:
            message = 'Storage integration is not supported yet'
            raise NotImplementedError(message)

    def read(self, keyed=False, limit=None, fail_fast=False):
        """Read table rows.

        Args:
            limit (int): return this amount of rows
            fail_fast (bool): raise first occured error

        Returns:
            tuple[]: table rows

        """

        # Collect rows
        count = 0
        errors = []
        result = []
        rows = self.iter(keyed=keyed)
        while True:
            try:
                row = next(rows)
                result.append(row)
                count += 1
                if count == limit:
                    break
            except exceptions.JsonTableSchemaException as exception:
                if fail_fast:
                    raise exception
                errors.append(exception)
            except StopIteration:
                break

        # Raise errors
        if errors:
            raise exceptions.MultipleInvalid(errors=errors)

        return result

    def save(self, target, backend=None, **options):
        """Save table rows.

        NOTE: To save schema use `table.schema.save(target)`

        Args:
            target (str): saving target
            backend (None/str): backend name like sql` or `bigquery`
            options (dict): tabulator options or backend options

        """
        message = 'Table saving is not supported yet'
        raise NotImplementedError(message)
