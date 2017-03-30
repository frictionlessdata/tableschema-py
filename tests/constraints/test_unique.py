# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import constraints


# Tests

@pytest.mark.parametrize('value, unique, result', [
    ('any', False, True),
    ('any', True, True),
])
def test_check_unique(value, unique, result):
    assert constraints.check_unique(value, unique) == result
