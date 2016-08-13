# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from tabulator import topen
from .model import SchemaModel


# Module API

class Table(object):
    """JSON Table Schema table representation.

    Args:
        source (mixed): data source
        schema (Schema/dict/str): schema instance, descriptor, path or url
        backend (None/str): backend name like sql` or `bigquery`
        options (dict): tabulator options or backend options

    """

    # Public

    def __init__(self, source, schema=None, backend=None, **options):

        # Instantiate schema
        self.__schema = None
        if schema is not None:
            self.__schema = SchemaModel(schema)

        # Use tabulator by default
        if backend is None:
            table = topen(source, with_headers=True, **options)

        # For storage backends
        else:
            pass

    @property
    def schema(self):
        """Schema: schema instance
        """
        return self.__schema

    @property
    def headers(self):
        pass

    @property
    def read(self, limit=None, fail_fast=False):
        """dict[]: table data
        """
        return list(self.iter())

    def iter(self, keyed=False):
        pass

    def save(self, target, backend=None, **options):
        pass
