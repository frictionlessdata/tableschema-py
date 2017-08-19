# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import copy
from tabulator import Stream
from functools import partial
from importlib import import_module
from .schema import Schema


# Module API

class Table(object):

    # Public

    def __init__(self, source, schema=None, strict=False,
                 post_cast=[], storage=None, **options):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Set attributes
        self.__source = source
        self.__stream = None
        self.__schema = None
        self.__headers = None
        self.__storage = None
        self.__post_cast = copy(post_cast)

        # Schema
        if schema is not None:
            self.__schema = Schema(schema)

        # Stream (tabulator)
        if storage is None:
            options.setdefault('headers', 1)
            self.__stream = Stream(source,  **options)

        # Stream (storage)
        else:
            module = 'tableschema.plugins.%s' % storage
            storage = import_module(module).Storage(**options)
            if self.__schema:
                storage.describe(source, self.__schema.descriptor)
            headers = Schema(storage.describe(source)).field_names
            self.__stream = Stream(partial(storage.iter, source), headers=headers)
            self.__storage = storage

    @property
    def headers(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__headers

    @property
    def schema(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__schema

    def iter(self, keyed=False, extended=False, cast=True):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        with self.__stream as stream:
            # TODO: remove reset after this issue will be resolved
            # https://github.com/frictionlessdata/tabulator-py/issues/190
            stream.reset()
            iterator = stream.iter(extended=True)
            iterator = self.__apply_processors(iterator, cast=cast)
            for row_number, headers, row in iterator:
                self.__headers = self.__headers or headers
                if extended:
                    yield (row_number, headers, row)
                elif keyed:
                    yield dict(zip(headers, row))
                else:
                    yield row

    def read(self, keyed=False, extended=False, cast=True, limit=None):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        result = []
        rows = self.iter(keyed=keyed, extended=extended, cast=cast)
        for count, row in enumerate(rows, start=1):
            result.append(row)
            if count == limit:
                break
        return result

    def infer(self, limit=100):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        if self.__schema is None or self.__headers is None:

            # Infer (tabulator)
            if not self.__storage:
                with self.__stream as stream:
                    # TODO: remove reset after this issue will be resolved
                    # https://github.com/frictionlessdata/tabulator-py/issues/190
                    stream.reset()
                    if self.__schema is None:
                        self.__schema = Schema()
                        self.__schema.infer(stream.sample[:limit], headers=stream.headers)
                    if self.__headers is None:
                        self.__headers = stream.headers

            # Infer (storage)
            else:
                descriptor = self.__storage.describe(self.__source)
                if self.__schema is None:
                    self.__schema = Schema(descriptor)
                if self.__headers is None:
                    self.__headers = self.__schema.field_names

        return self.__schema.descriptor

    def save(self, target, storage=None, **options):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Save (tabulator)
        if storage is None:
            with Stream(self.iter, headers=self.__schema.headers) as stream:
                stream.save(target, **options)
            return True

        # Save (storage)
        else:
            module = 'tableschema.plugins.%s' % storage
            storage = import_module(module).Storage(**options)
            storage.create(target, self.__schema.descriptor, force=True)
            storage.write(target, self.iter())
            return storage

    # Internal

    def __apply_processors(self, iterator, cast=True):

        # Apply processors to iterator
        def builtin_processor(extended_rows):
            for row_number, headers, row in extended_rows:
                if self.__schema and cast:
                    row = self.__schema.cast_row(row)
                yield (row_number, headers, row)
        processors = [builtin_processor] + self.__post_cast
        for processor in processors:
            iterator = processor(iterator)

        return iterator
