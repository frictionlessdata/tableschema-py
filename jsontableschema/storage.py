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
    """Tabular Storage interface.

    Concrete backends shouldn't inherit from this base class
    to simplify maintenance. Just use as a reference.

    Args:
        options (dict): concrete backend options

    """

    # Public

    @abstractmethod
    def __init__(self, **options):
        pass

    @property
    def buckets(self):
        """str[]: list of buckets.

        This list should be sorted in order of foreign key dependency.
        (direct order for creation and reverse order for deletion)

        """
        pass

    @abstractmethod
    def create(self, bucket, descriptor, force=False):
        """Create one/few buckets.

        Args:
            bucket (str/list): bucket name or list of bucket names
            descriptor (dict/dict[]): schema descriptor or list of descriptors
            force (bool): delete and re-create already existent buckets

        Raises:
            StorageError: if table already exists.

        """
        pass

    def delete(self, bucket=None, ignore=False):
        """Delete one/few/all bucket(s).

        Args:
            bucket (str/list/None): bucket name or list of bucket
                names to delete. If None all buckets will be deleted.
            ignore (bool): don't raise an error on non-existent bucket
                deletion from storage

        Raises:
            StorageError: if table doesn't exist and ignore is False

        """
        pass

    def describe(self, bucket, descriptor=None):
        """Get/set bucket's schema descriptor.

        Args:
            table (str): bucket name
            schema (dict): schema descriptor to set

        Returns:
            dict: bucket's schema descriptor

        """
        pass

    def iter(self, bucket):
        """Yields bucket rows.

        This method should return typed values
        based on the schema of this buckets.

        Args:
            bucket (str): bucket name

        Yields:
            list: bucket row

        """
        pass

    def read(self, bucket):
        """Read rows from bucket.

        This method should return typed values
        based on the schema of this buckets.

        Args:
            bucket (str): bucket name

        Returns:
            list[]: bucket rows

        """
        pass

    def write(self, bucket, rows):
        """Write rows to bucket.

        This method should store values of unsupported
        types as strings internally (like csv does).

        Args:
            bucket (str): bucket name
            rows (list[]): rows to write

        """
        pass
