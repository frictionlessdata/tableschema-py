# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    (True, True),
    ('yes', True),
    ('y', True),
    ('true', True),
    ('t', True),
    ('1', True),
    ('YES', True),
    ('Yes', True),
    (False, False),
    ('no', False),
    ('n', False),
    ('false', False),
    ('f', False),
    ('0', False),
    ('NO', False),
    ('No', False),
    (0, ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_boolean_default(value, result):
    assert types.cast_boolean_default(value) == result
