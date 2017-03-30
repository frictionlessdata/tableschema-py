# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from datetime import datetime
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    (datetime(2014, 1, 1, 6), datetime(2014, 1, 1, 6)),
    ('2014-01-01T06:00:00Z', datetime(2014, 1, 1, 6)),
    ('Mon 1st Jan 2014 9 am', ERROR),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_datetime_default(value, result):
    assert types.cast_datetime_default(value) == result


@pytest.mark.parametrize('value, pattern, result', [
    (datetime(2006, 11, 21, 16, 30), '%d/%m/%y %H:%M', datetime(2006, 11, 21, 16, 30)),
    ('21/11/06 16:30', '%d/%m/%y %H:%M', datetime(2006, 11, 21, 16, 30)),
    ('21/11/06 16:30', '%H:%M %d/%m/%y', ERROR),
    ('21/11/06 16:30', 'invalid', ERROR),
    ('invalid', '%H:%M %d/%m/%y', ERROR),
    (True, '%H:%M %d/%m/%y', ERROR),
    ('', '%H:%M %d/%m/%y', ERROR),
])
def test_cast_datetime_pattern(value, pattern, result):
    assert types.cast_datetime_pattern(value, pattern) == result


@pytest.mark.parametrize('value, result', [
    (datetime(2014, 1, 1, 6), datetime(2014, 1, 1, 6)),
    ('10th Jan 1969 9 am', datetime(1969, 1, 10, 9)),
    ('invalid', ERROR),
    (True, ERROR),
    ('', ERROR),
])
def test_cast_datetime_any(value, result):
    assert types.cast_datetime_any(value) == result
