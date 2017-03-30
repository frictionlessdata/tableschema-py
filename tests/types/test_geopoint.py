# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('value, result', [
    ({'lon': 180, 'lat': 90}, {'lon': 180, 'lat': 90}),
    ('180,90', {'lon': 180, 'lat': 90}),
    ('180, -90', {'lon': 180, 'lat': -90}),
    ('181,90', ERROR),
    ('0,91', ERROR),
    ('string', ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_geopoint_default(value, result):
    assert types.cast_geopoint_default(value) == result


@pytest.mark.parametrize('value, result', [
    ({'lon': 180, 'lat': 90}, {'lon': 180, 'lat': 90}),
    ('[180, -90]', {'lon': 180, 'lat': -90}),
    ([181, 90], ERROR),
    ([0, 91], ERROR),
    ('180,90', ERROR),
    ('string', ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_geopoint_array(value, result):
    assert types.cast_geopoint_array(value) == result


@pytest.mark.parametrize('value, result', [
    ({'lon': 180, 'lat': 90}, {'lon': 180, 'lat': 90}),
    ('{"lon": 180, "lat": 90}', {'lon': 180, 'lat': 90}),
    ({'lon': 181, 'lat': 90}, ERROR),
    ({'lon': 180, 'lat': -91}, ERROR),
    ([180, -90], ERROR),
    ('180,90', ERROR),
    ('string', ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_geopoint_object(value, result):
    assert types.cast_geopoint_object(value) == result
