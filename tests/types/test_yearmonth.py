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
    ('default', 10, 10),
    ('default', '10', 10),
    ('default', -10, ERROR),
    ('default', 20, ERROR),
    ('default', '3.14', ERROR),
    ('default', '', ERROR),
])
def test_cast_yearmonth(format, value, result):
    assert types.cast_yearmonth(format, value) == result
