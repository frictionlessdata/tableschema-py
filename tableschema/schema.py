# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import six
import json
from copy import deepcopy
from .profile import Profile
from .field import Field
from . import exceptions
from . import helpers
from . import config
from . import types


# Module API

class Schema(object):

    # Public

    def __init__(self, descriptor={}, strict=False):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Process descriptor
        descriptor = helpers.retrieve_descriptor(descriptor)

        # Set attributes
        self.__strict = strict
        self.__current_descriptor = deepcopy(descriptor)
        self.__next_descriptor = deepcopy(descriptor)
        self.__profile = Profile('table-schema')
        self.__errors = []
        self.__fields = []

        # Build instance
        self.__build()

    @property
    def valid(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return not bool(self.__errors)

    @property
    def errors(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__errors

    @property
    def descriptor(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        # Never use this.descriptor inside this class (!!!)
        return self.__next_descriptor

    @property
    def primary_key(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        primary_key = self.__current_descriptor.get('primaryKey', [])
        if not isinstance(primary_key, list):
            primary_key = [primary_key]
        return primary_key

    @property
    def foreign_keys(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        foreign_keys = self.__current_descriptor.get('foreignKeys', [])
        for key in foreign_keys:
            key.setdefault('fields', [])
            key.setdefault('reference', {})
            key['reference'].setdefault('resource', '')
            key['reference'].setdefault('fields', [])
            if not isinstance(key['fields'], list):
                key['fields'] = [key['fields']]
            if not isinstance(key['reference']['fields'], list):
                key['reference']['fields'] = [key['reference']['fields']]
        return foreign_keys

    @property
    def fields(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return self.__fields

    @property
    def field_names(self):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        return [field.name for field in self.fields]

    def get_field(self, name):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def add_field(self, descriptor):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        self.__current_descriptor.setdefault('fields', [])
        self.__current_descriptor['fields'].append(descriptor)
        self.__build()
        return self.__fields[-1]

    def remove_field(self, name):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        field = self.get_field(name)
        if field:
            predicat = lambda field: field.get('name') != name
            self.__current_descriptor['fields'] = filter(
                predicat, self.__current_descriptor['fields'])
            self.__build()
        return field

    def cast_row(self, row, fail_fast=False):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Prepare
        result = []
        errors = []

        # Check row length
        if len(row) != len(self.fields):
            message = 'Row length %s doesn\'t match fields count %s'
            message = message % (len(row), len(self.fields))
            raise exceptions.CastError(message)

        # Cast row
        for field, value in zip(self.fields, row):
            try:
                result.append(field.cast_value(value))
            except exceptions.CastError as exception:
                if fail_fast:
                    raise
                errors.append(exception)

        # Raise errors
        if errors:
            message = 'There are %s cast errors (see exception.errors)' % len(errors)
            raise exceptions.CastError(message, errors=errors)

        return result

    def infer(self, rows, headers=1, confidence=0.75):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """

        # Get headers
        if isinstance(headers, int):
            headers_row = headers
            while True:
                headers_row -= 1
                headers = rows.pop(0)
                if not headers_row:
                    break
        elif not isinstance(headers, list):
            headers = []

        # Get descriptor
        guesser = _TypeGuesser()
        resolver = _TypeResolver()
        descriptor = {'fields': []}
        type_matches = {}
        for header in headers:
            descriptor['fields'].append({'name': header})
        for index, row in enumerate(rows):
            # Normalize rows with invalid dimensions for sanity
            row_length = len(row)
            headers_length = len(headers)
            if row_length > headers_length:
                row = row[:len(headers)]
            if row_length < headers_length:
                diff = headers_length - row_length
                fill = [''] * diff
                row = row + fill
            # build a column-wise lookup of type matches
            for index, value in enumerate(row):
                rv = guesser.cast(value)
                if type_matches.get(index):
                    type_matches[index].extend(rv)
                else:
                    type_matches[index] = list(rv)
        # choose a type/format for each column based on the matches
        for index, results in type_matches.items():
            rv = resolver.get(results, confidence)
            descriptor['fields'][index].update(**rv)

        # Save descriptor
        self.__current_descriptor = descriptor
        self.__build()

        return descriptor

    def commit(self, strict=None):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        if strict is not None:
            self.__strict = strict
        elif self.__current_descriptor == self.__next_descriptor:
            return False
        self.__current_descriptor = deepcopy(self.__next_descriptor)
        self.__build()
        return True

    def save(self, target, ensure_ascii=True):
        """https://github.com/frictionlessdata/tableschema-py#schema
        """
        mode = 'w'
        encoding = 'utf-8'
        if six.PY2:
            mode = 'wb'
            encoding = None
        helpers.ensure_dir(target)
        with io.open(target, mode=mode, encoding=encoding) as file:
            json.dump(self.__current_descriptor, file, indent=4, ensure_ascii=ensure_ascii)

    # Internal

    def __build(self):

        # Process descriptor
        expand = helpers.expand_schema_descriptor
        self.__current_descriptor = expand(self.__current_descriptor)
        self.__next_descriptor = deepcopy(self.__current_descriptor)

        # Validate descriptor
        try:
            self.__profile.validate(self.__current_descriptor)
            self.__errors = []
        except exceptions.ValidationError as exception:
            self.__errors = exception.errors
            if self.__strict:
                raise exception

        # Populate fields
        self.__fields = []
        for field in self.__current_descriptor.get('fields', []):
            missing_values = self.__current_descriptor['missingValues']
            try:
                field = Field(field, missing_values=missing_values)
            except Exception:
                field = False
            self.__fields.append(field)

    # Deprecated

    headers = field_names
    has_field = get_field


# Internal

_INFER_TYPE_ORDER = [
    'duration',
    'geojson',
    'geopoint',
    'object',
    'array',
    'datetime',
    'time',
    'date',
    'integer',
    'number',
    'boolean',
    'string',
    'any',
]


class _TypeGuesser(object):
    """Guess the type for a value returning a tuple of ('type', 'format')
    """

    # Public

    def cast(self, value):
        for priority, name in enumerate(_INFER_TYPE_ORDER):
            cast = getattr(types, 'cast_%s' % name)
            result = cast('default', value)
            if result != config.ERROR:
                yield (name, 'default', priority)


class _TypeResolver(object):
    """Get the best matching type/format from a list of possible ones.
    """

    # Public

    def get(self, results, confidence):
        variants = set(results)
        # only one candidate... that's easy.
        if len(variants) == 1:
            rv = {'type': results[0][0], 'format': results[0][1]}
        else:
            counts = {}
            for result in results:
                if counts.get(result):
                    counts[result] += 1
                else:
                    counts[result] = 1
            # tuple representation of `counts` dict sorted by values
            sorted_counts = sorted(counts.items(),
                                   key=lambda item: item[1],
                                   reverse=True)
            # Allow also counts that are not the max, based on the confidence
            max_count = sorted_counts[0][1]
            sorted_counts = filter(lambda item: item[1] >= max_count * confidence,
                                   sorted_counts)
            # Choose the most specific data type
            sorted_counts = sorted(sorted_counts,
                                   key=lambda item: item[0][2])
            rv = {'type': sorted_counts[0][0][0], 'format': sorted_counts[0][0][1]}
        return rv
