# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from datetime import date
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    (date(2019, 1, 1), date(2019, 1, 1)),
    ('2019-01-01', date(2019, 1, 1)),
    ('10th Jan 1969', ERROR),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_date_default(value, result):
    assert types.cast_date_default(value) == result


@pytest.mark.parametrize('value, result', [
    (date(2019, 1, 1), date(2019, 1, 1)),
    ('2019-01-01', date(2019, 1, 1)),
    ('10th Jan 1969', date(1969, 1, 10)),
    ('10th Jan nineteen sixty nine', ERROR),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_date_any(value, result):
    assert types.cast_date_any(value) == result


@pytest.mark.parametrize('value, pattern, result', [
    (date(2019, 1, 1), '%d/%m/%y', date(2019, 1, 1)),
    ('21/11/06', '%d/%m/%y', date(2006, 11, 21)),
    ('21/11/06 16:30', '%y/%m/%d', ERROR),
    ('21/11/06 16:30', 'invalid', ERROR),
    ('invalid', '%d/%m/%y', ERROR),
    (True, '%d/%m/%y', ERROR),
    ('', '%d/%m/%y', ERROR),
])
def test_cast_date_pattern(value, pattern, result):
    assert types.cast_date_pattern(value, pattern) == result
