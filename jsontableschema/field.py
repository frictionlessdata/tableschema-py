# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# Module API

class Field(object):
    """JSON Table Schema field representation.
    """

    def __init__(self, descriptor):
        self.__descriptor = descriptor

    @property
    def descriptor(self):
        return self.__descriptor

    @property
    def name(self):
        return self.__descriptor['name']

    @property
    def type(self):
        return self.__descriptor.get('type', 'string')

    @property
    def format(self):
        return self.__descriptor.get('format', 'default')

    @property
    def constraints(self):
        return self.__descriptor.get('constraints', {})

    def convert_value(self, value):
        return value
