# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, minLength, result', [
    ([1], 0, True),
    ([1], 1, True),
    ([1], 2, False),
])
def test_check_minLength(value, minLength, result):
    assert constraints.check_minLength(value, minLength) == result
