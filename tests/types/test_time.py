# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from datetime import time
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    (time(6), time(6)),
    ('06:00:00', time(6)),
    ('09:00', ERROR),
    ('3 am', ERROR),
    ('3.00', ERROR),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_time_default(value, result):
    assert types.cast_time_default(value) == result


@pytest.mark.parametrize('value, result', [
    (time(6), time(6)),
    ('06:00:00', time(6)),
    ('3:00 am', time(3)),
    ('some night', ERROR),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_time_any(value, result):
    assert types.cast_time_any(value) == result


@pytest.mark.parametrize('value, pattern, result', [
    (time(6), '%H:%M', time(6)),
    ('06:00', '%H:%M', time(6)),
    ('06:50', '%M:%H', ERROR),
    ('3:00 am', '%H:%M', ERROR),
    ('some night', '%H:%M', ERROR),
    ('invalid', '%H:%M', ERROR),
    (True, '%H:%M', ERROR),
    ('', '%H:%M', ERROR),
])
def test_cast_time_pattern(value, pattern, result):
    assert types.cast_time_pattern(value, pattern) == result
