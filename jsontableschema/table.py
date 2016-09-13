# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import unicodecsv
from tabulator import Stream
from functools import partial
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

        # Tabulator
        if backend is None:
            options.setdefault('headers', 1)
            self.__stream = Stream(source,  **options)
            self.__stream.open()
            if self.__schema is None:
                self.__schema = Schema(infer(
                    self.__stream.headers, self.__stream.sample))

        # Storage
        else:
            module = 'jsontableschema.plugins.%s' % backend
            storage = import_module(module).Storage(**options)
            generator = partial(storage.iter, source)
            if self.__schema is None:
                self.__schema = Schema(storage.describe(source))
            storage.describe(source, self.__schema.descriptor)
            self.__stream = Stream(generator, headers=self.__schema.headers)
            self.__stream.open()

        # Processors
        def builtin_processor(extended_rows):
            for number, headers, row in extended_rows:
                headers = self.__schema.headers
                row = self.__schema.convert_row(row)
                yield (number, headers, row)
        self.__stream.post_parse.append(builtin_processor)
        self.__stream.post_parse.extend(post_convert)

    @property
    def post_convert(self):
        """func[]: processors
        """
        return self.__post_convert

    @property
    def stream(self):
        """tabulator.Stream: stream instance
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
        self.__stream.reset()
        return self.__stream.iter(
            keyed=keyed, extended=extended)

    def read(self, keyed=False, extended=False, limit=None):
        """Read table rows.

        Args:
            limit (int): return this amount of rows

        Returns:
            tuple[]: table rows

        """
        self.__stream.reset()
        return self.__stream.read(
            keyed=keyed, extended=extended, limit=limit)

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
            self.__stream.reset()
            self.__stream.save(target, **options)

        # Storage
        else:
            self.__stream.reset()
            module = 'jsontableschema.plugins.%s' % backend
            storage = import_module(module).Storage(**options)
            storage.create(target, self.schema.descriptor, force=True)
            storage.write(target, self.iter())
            return storage
