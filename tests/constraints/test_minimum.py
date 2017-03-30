# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, minimum, result', [
    (1, 0, True),
    (1, 1, True),
    (1, 2, False),
])
def test_check_minimum(value, minimum, result):
    assert constraints.check_minimum(value, minimum) == result
