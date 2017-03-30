# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, enum, result', [
    (1, [1, 2], True),
    (1, [0, 2], False),
    (1, [], False),
])
def test_check_enum(value, enum, result):
    assert constraints.check_enum(value, enum) == result
