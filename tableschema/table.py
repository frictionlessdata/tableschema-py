# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from copy import copy
from tabulator import Stream
from functools import partial
from collections import OrderedDict
from .storage import Storage
from .schema import Schema
from . import exceptions


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
        if isinstance(schema, Schema):
            self.__schema = schema
        elif schema is not None:
            self.__schema = Schema(schema)

        # Stream (tabulator)
        if storage is None:
            options.setdefault('headers', 1)
            self.__stream = Stream(source,  **options)

        # Stream (storage)
        else:
            if not isinstance(storage, Storage):
                storage = Storage.connect(storage, **options)
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

    def iter(self, keyed=False, extended=False, cast=True, relations=False):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Prepare unique checks
        if cast:
            unique_fields_cache = {}
            if self.schema:
                unique_fields_cache = _create_unique_fields_cache(self.schema)

        # Open/iterate stream
        self.__stream.open()
        iterator = self.__stream.iter(extended=True)
        iterator = self.__apply_processors(iterator, cast=cast)
        for row_number, headers, row in iterator:

            # Get headers
            if not self.__headers:
                self.__headers = headers

            # Check headers
            if cast:
                if self.schema and self.headers:
                    if self.headers != self.schema.field_names:
                        self.__stream.close()
                        message = 'Table headers don\'t match schema field names'
                        raise exceptions.CastError(message)

            # Check unique
            if cast:
                for indexes, cache in unique_fields_cache.items():
                    values = tuple(value for i, value in enumerate(row) if i in indexes)
                    if not all(map(lambda value: value is None, values)):
                        if values in cache['data']:
                            self.__stream.close()
                            message = 'Field(s) "%s" duplicates in row "%s"'
                            message = message % (cache['name'], row_number)
                            raise exceptions.CastError(message)
                        cache['data'].add(values)

            # Resolve relations
            if relations:
                if self.schema:
                    for foreign_key in self.schema.foreign_keys:
                        row = _resolve_relations(row, headers, relations, foreign_key)
                        if row is None:
                            self.__stream.close()
                            message = 'Foreign key "%s" violation in row "%s"'
                            message = message % (foreign_key['fields'], row_number)
                            raise exceptions.RelationError(message)

            # Form row
            if extended:
                yield (row_number, headers, row)
            elif keyed:
                yield dict(zip(headers, row))
            else:
                yield row

        # Close stream
        self.__stream.close()

    def read(self, keyed=False, extended=False, cast=True, relations=False, limit=None):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        result = []
        rows = self.iter(keyed=keyed, extended=extended, cast=cast, relations=relations)
        for count, row in enumerate(rows, start=1):
            result.append(row)
            if count == limit:
                break
        return result

    def infer(self, limit=100, confidence=0.75):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        if self.__schema is None or self.__headers is None:

            # Infer (tabulator)
            if not self.__storage:
                with self.__stream as stream:
                    if self.__schema is None:
                        self.__schema = Schema()
                        self.__schema.infer(stream.sample[:limit],
                                            headers=stream.headers,
                                            confidence=confidence)
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
            if not isinstance(storage, Storage):
                storage = Storage.connect(storage, **options)
            storage.create(target, self.__schema.descriptor, force=True)
            storage.write(target, self.iter(cast=False))
            return storage

    # Private

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


# Internal

def _create_unique_fields_cache(schema):
    primary_key_indexes = []
    cache = {}

    # Unique
    for index, field in enumerate(schema.fields):
        if field.name in schema.primary_key:
            primary_key_indexes.append(index)
        if field.constraints.get('unique'):
            cache[tuple([index])] = {
                'name': field.name,
                'data': set(),
            }

    # Primary key
    if primary_key_indexes:
        cache[tuple(primary_key_indexes)] = {
            'name': ', '.join(schema.primary_key),
            'data': set(),
        }

    return cache


def _resolve_relations(row, headers, relations, foreign_key):

    # Prepare helpers - needed data structures
    keyed_row = OrderedDict(zip(headers, row))
    fields = list(zip(foreign_key['fields'], foreign_key['reference']['fields']))
    reference = relations.get(foreign_key['reference']['resource'])
    if not reference:
        return row

    # Collect values - valid if all None
    values = {}
    valid = True
    for field, ref_field in fields:
        if field and ref_field:
            values[ref_field] = keyed_row[field]
            if keyed_row[field] is not None:
                valid = False

    # Resolve values - valid if match found
    if not valid:
        for refValues in reference:
            if set(values.items()).issubset(set(refValues.items())):
                for field, ref_field in fields:
                    keyed_row[field] = refValues
                valid = True
                break

    return list(keyed_row.values()) if valid else None
