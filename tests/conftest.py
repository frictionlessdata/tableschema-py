# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from copy import deepcopy


# Fixtures

@pytest.fixture(scope='session')
def apply_defaults():
    def function(descriptor):
        descriptor = deepcopy(descriptor)
        # Schema descriptor
        if descriptor.get('fields'):
            descriptor.setdefault('missingValues', [''])
            for field in descriptor['fields']:
                field.setdefault('type', 'string')
                field.setdefault('format', 'default')
        # Field descriptor
        else:
            descriptor.setdefault('type', 'string')
            descriptor.setdefault('format', 'default')
        return descriptor
    return function
