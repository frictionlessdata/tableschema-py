# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import isodate
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    (isodate.Duration(years=1), isodate.Duration(years=1)),
    ('P1Y10M3DT5H11M7S',
        isodate.Duration(years=1, months=10, days=3, hours=5, minutes=11, seconds=7)),
    ('P1Y', isodate.Duration(years=1)),
    ('P1M', isodate.Duration(months=1)),
    ('P1D', isodate.Duration(days=1)),
    ('PT1H', isodate.Duration(hours=1)),
    ('PT1M', isodate.Duration(minutes=1)),
    ('PT1S', isodate.Duration(seconds=1)),
    ('P1M1Y', ERROR),
    ('P-1Y', ERROR),
    (True, ERROR),
    (1, ERROR),
    ('', ERROR),
])
def test_cast_duration_default(value, result):
    assert types.cast_duration_default(value) == result
