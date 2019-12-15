# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import warnings
from .table import Table


# Module API

def infer(source, headers=1, limit=100, confidence=0.75, **options):
    """Infer source schema.

    # Arguments
        source (any): source as path, url or inline data
        headers (int/str[]): headers rows number or headers list
        confidence (float): how many casting errors are allowed (as a ratio, between 0 and 1)

    # Raises
        TableSchemaException: raises any error that occurs during the process

    # Returns
        dict: returns schema descriptor

    """

    # Deprecated arguments order
    is_string = lambda value: isinstance(value, six.string_types)
    if isinstance(source, list) and all(map(is_string, source)):
        warnings.warn('Correct arguments order infer(source, headers)', UserWarning)
        source, headers = headers, source

    table = Table(source, headers=headers, **options)
    descriptor = table.infer(limit=limit, confidence=confidence)
    return descriptor
