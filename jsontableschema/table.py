# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import unicodecsv
from tabulator import topen
from importlib import import_module
from .schema import Schema
from .infer import infer
from . import exceptions
from . import utilities
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

    def __init__(self, source, schema=None, post_convert=None,
                 backend=None, **options):

        # Initiate if None
        if post_convert is None:
            post_convert = []

        # Instantiate schema
        if isinstance(schema, (compat.str, dict)):
            schema = Schema(schema)

        # Instantiate storage
        storage = None
        if backend is not None:
            module = 'jsontableschema.plugins.%s' % backend
            storage = import_module(module).Storage(**options)
            # https://github.com/frictionlessdata/jsontableschema-py/issues/70
            # if schema is not None:
            #     storage.describe(source, schema)

        # Set attributes
        self.__source = source
        self.__schema = schema
        self.__storage = storage
        self.__options = options
        self.__post_convert = post_convert

    @property
    def schema(self):
        """Schema: schema instance
        """
        if self.__schema is None:
            self.__schema = self.__infer_schema()
        return self.__schema

    def iter(self, keyed=False, extended=False):
        """Yields table rows.

        Args:
            keyed (bool): yield keyed rows
            extended (bool): yield extended rows

        Yields:
            mixed[]/mixed{}: row or keyed row or extended row

        """
        extended_rows = self.__iter_extended_rows()
        for processor in self.__post_convert:
            extended_rows = processor(extended_rows)
        for number, headers, row in extended_rows:
            if extended:
                yield (number, headers, row)
            elif keyed:
                yield dict(zip(headers, row))
            else:
                yield row

    def read(self, keyed=False, extended=False, limit=None, fail_fast=False):
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
        rows = self.iter(keyed=keyed, extended=extended)
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

        Returns:
            None/Storage: storage instance if backend used

        """

        # Tabulator
        if backend is None:
            # It's temporal for now supporting only csv
            # https://github.com/frictionlessdata/tabulator-py/issues/36
            utilities.ensure_dir(target)
            with io.open(target, 'wb') as file:
                writer = unicodecsv.writer(file, encoding='utf-8')
                writer.writerow(self.schema.headers)
                for row in self.iter():
                    writer.writerow(row)

        # Storage
        if backend is not None:
            module = 'jsontableschema.plugins.%s' % backend
            storage = import_module(module).Storage(**options)
            if storage.check(target):
                storage.delete(target)
            storage.create(target, self.schema.descriptor)
            storage.write(target, self.iter())
            return storage

    # Private

    def __infer_schema(self):

        # Tabulator
        if self.__storage is None:
            options = {}
            options.update(headers='row1')
            options.update(self.__options)
            with topen(self.__source, **options) as table:
                descriptor = infer(table.headers, table.sample)
            return Schema(descriptor)

        # Storage
        else:
            return Schema(self.__storage.describe(self.__source))

    def __iter_extended_rows(self):

        # Tabulator
        if self.__storage is None:
            options = {}
            options.update(headers='row1')
            options.update(self.__options)
            with topen(self.__source, **options) as table:
                for number, headers, row in table.iter(extended=True):
                    row = self.schema.convert_row(row)
                    yield (number, self.schema.headers, row)

        # Storage
        else:
            rows = self.__storage.read(self.__source)
            for number, row in enumerate(rows, start=1):
                row = self.schema.convert_row(row)
                yield (number, self.schema.headers, row)
