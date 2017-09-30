# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from importlib import import_module
from abc import ABCMeta, abstractmethod
from . import exceptions


# Module API

@add_metaclass(ABCMeta)
class Storage(object):

    # Public

    @classmethod
    def connect(cls, name, **options):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        if cls is not Storage:
            message = 'Storage.connect is not available on concrete implemetations'
            raise exceptions.StorageError(message)
        module = 'tableschema.plugins.%s' % name
        storage = import_module(module).Storage(**options)
        return storage

    @abstractmethod
    def __init__(self, **options):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @property
    @abstractmethod
    def buckets(self):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def create(self, bucket, descriptor, force=False):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def delete(self, bucket=None, ignore=False):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def describe(self, bucket, descriptor=None):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def iter(self, bucket):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def read(self, bucket):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass

    @abstractmethod
    def write(self, bucket, rows):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        pass
