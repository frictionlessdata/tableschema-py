# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from six import add_metaclass
from importlib import import_module
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Storage(object):

    # Public

    def __new__(cls, *args, **kwargs):
        """https://github.com/frictionlessdata/tableschema-py#storage
        """
        if cls is Storage:
            module = 'tableschema.plugins.%s' % args[0]
            storage = import_module(module).Storage(*args[1:], **kwargs)
            return storage
        return object.__new__(cls)

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
