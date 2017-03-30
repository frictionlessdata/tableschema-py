# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, pattern, result', [
    ('test', '^test$', True),
    ('TEST', '^test$', False),
])
def test_check_pattern(value, pattern, result):
    assert constraints.check_pattern(value, pattern) == result
