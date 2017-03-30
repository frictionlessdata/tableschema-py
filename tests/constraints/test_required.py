# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, required, result', [
    (1, False, True),
    (0, True, True),
    (None, True, False),
])
def test_check_required(value, required, result):
    assert constraints.check_required(value, required) == result
