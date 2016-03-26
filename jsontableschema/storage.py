# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Storage(object):
    """Tabular Storage Interface.

    Parameters
    ----------
    prefix: str
        Prefix for all tables.
    options: dict
        Concrete implementations options.

    """

    # Public

    @abstractmethod
    def __init__(self, prefix='', **options):
        pass  # pragma: no cover

    @property
    def tables(self):
        """Return list of storage's table names.

        Returns
        -------
        str[]
            List of table names.

        """
        pass  # pragma: no cover

    @abstractmethod
    def check(self, table):
        """Return true if table exists.

        Parameters
        ----------
        table: str
            Table name.

        Returns
        -------
        bool
            Table existence.

        """
        pass  # pragma: no cover

    @abstractmethod
    def create(self, table, schema):
        """Create table by schema.

        Parameters
        ----------
        table: str/list
            Table name or list of table names.
        schema: dict/list
            JSONTableSchema schema or list of schemas.

        Raises
        ------
        RuntimeError
            If table already exists.

        """
        pass  # pragma: no cover

    def delete(self, table):
        """Delete table.

        Parameters
        ----------
        table: str/list
            Table name or list of table names.

        Raises
        ------
        RuntimeError
            If table doesn't exist.

        """

    def describe(self, table):
        """Return table's JSONTableSchema schema.

        Parameters
        ----------
        table: str
            Table name.

        Returns
        -------
        dict
            JSONTableSchema schema.

        """

    def read(self, table):
        """Read data from table.

        Parameters
        ----------
        table: str
            Table name.

        Returns
        -------
        iterable
            Data tuples iterable.

        """

    def write(self, table, data):
        """Write data to table.

        Parameters
        ----------
        table: str
            Table name.
        data: iterable
            Iterable of data tuples.

        """
