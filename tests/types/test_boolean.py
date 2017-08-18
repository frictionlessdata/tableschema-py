# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('format, value, options, result', [
    ('default', True, {}, True),
    ('default', 'true', {}, True),
    ('default', 'True', {}, True),
    ('default', 'TRUE', {}, True),
    ('default', '1', {}, True),
    ('default', 'yes', {'trueValues': ['yes']}, True),
    ('default', False, {}, False),
    ('default', 'false', {}, False),
    ('default', 'False', {}, False),
    ('default', 'FALSE', {}, False),
    ('default', '0', {}, False),
    ('default', 'no', {'falseValues': ['no']}, False),
    ('default', 't', {}, ERROR),
    ('default', 'YES', {}, ERROR),
    ('default', 'Yes', {}, ERROR),
    ('default', 'f', {}, ERROR),
    ('default', 'NO', {}, ERROR),
    ('default', 'No', {}, ERROR),
    ('default', 0, {}, ERROR),
    ('default', 1, {}, ERROR),
    ('default', '3.14', {}, ERROR),
    ('default', '', {}, ERROR),
    ('default', 'Yes', {'trueValues': ['yes']}, ERROR),
    ('default', 'No', {'falseValues': ['no']}, ERROR),
])
def test_cast_boolean(format, value, options, result):
    assert types.cast_boolean(format, value, **options) == result
