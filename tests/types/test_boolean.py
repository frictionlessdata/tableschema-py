# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('format, value, result', [
    ('default', True, True),
    ('default', 'yes', True),
    ('default', 'y', True),
    ('default', 'true', True),
    ('default', 't', True),
    ('default', '1', True),
    ('default', 'YES', True),
    ('default', 'Yes', True),
    ('default', False, False),
    ('default', 'no', False),
    ('default', 'n', False),
    ('default', 'false', False),
    ('default', 'f', False),
    ('default', '0', False),
    ('default', 'NO', False),
    ('default', 'No', False),
    ('default', 0, ERROR),
    ('default', 1, ERROR),
    ('default', '3.14', ERROR),
    ('default', '', ERROR),
])
def test_cast_boolean(format, value, result):
    assert types.cast_boolean(format, value) == result
