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
    (10, 10),
    ('10', 10),
    (-10, ERROR),
    (20, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_yearmonth_default(value, result):
    assert types.cast_yearmonth_default(value) == result
