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
    ('default', 1, 1),
    ('default', '1', 1),
    ('default', '3.14', ERROR),
    ('default', '', ERROR),
])
def test_cast_integer(format, value, result):
    assert types.cast_integer(format, value) == result
