# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, maxLength, result', [
    ([1], 0, False),
    ([1], 1, True),
    ([1], 2, True),
])
def test_check_maxLength(value, maxLength, result):
    assert constraints.check_maxLength(value, maxLength) == result
