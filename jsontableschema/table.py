# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import unicodecsv
from tabulator import Stream
from importlib import import_module
from .schema import Schema
from .infer import infer
from . import helpers
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

        # Defaults
        if post_convert is None:
            post_convert = []

        # Schema
        self.__schema = None
        if isinstance(schema, (compat.str, dict)):
            self.__schema = Schema(schema)

        # Stream
        self.__stream = None
        if backend is None:
            options.setdefault('headers', 1)
            self.__stream = Stream(source,  **options)
            self.__stream.open()
            if self.__schema is None:
                self.__schema = Schema(infer(
                    self.__stream.headers, self.__stream.sample))

        # Storage
        self.__storage = None
        if backend is not None:
            module = 'jsontableschema.plugins.%s' % backend
            self.__storage = import_module(module).Storage(**options)
            if self.__schema is None:
                self.__schema = Schema(self.__storage.describe(source))
            else:
                self.__storage.describe(source, self.__schema.descriptor)

        # Attributes
        self.__source = source
        self.__post_convert = post_convert

    @property
    def stream(self):
        """tabulator.Stream/None: stream instance
        """
        return self.__stream

    @property
    def schema(self):
        """Schema: schema instance
        """
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

    def read(self, keyed=False, extended=False, limit=None):
        """Read table rows.

        Args:
            limit (int): return this amount of rows

        Returns:
            tuple[]: table rows

        """
        result = []
        rows = self.iter(keyed=keyed, extended=extended)
        for count, row in enumerate(rows, start=1):
            result.append(row)
            if count == limit:
                break
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

        # Stream
        if backend is None:
            self.stream.reset()
            self.stream.save(target, **options)

        # Storage
        else:
            module = 'jsontableschema.plugins.%s' % backend
            storage = import_module(module).Storage(**options)
            if storage.check(target):
                storage.delete(target)
            storage.create(target, self.schema.descriptor)
            storage.write(target, self.iter())
            return storage

    # Private

    def __iter_extended_rows(self):

        # Stream
        if self.stream is not None:
            self.stream.reset()
            for number, headers, row in self.stream.iter(extended=True):
                row = self.schema.convert_row(row)
                yield (number, self.schema.headers, row)

        # Storage
        else:
            rows = self.__storage.iter(self.__source)
            for number, row in enumerate(rows, start=1):
                row = self.schema.convert_row(row)
                yield (number, self.schema.headers, row)
