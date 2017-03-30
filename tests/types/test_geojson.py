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
    ({'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None},
        {'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None}),
    ('{"geometry": null, "type": "Feature", "properties": {"\\u00c3": "\\u00c3"}}',
        {'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None}),
    ({'coordinates': [0, 0, 0], 'type': 'Point'}, ERROR),
    ('string', ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
    ({}, ERROR),
    ('{}', ERROR),
])
def test_cast_geojson_default(value, result):
    assert types.cast_geojson_default(value) == result


@pytest.mark.parametrize('value, result', [
    ({'type': 'LineString', 'arcs': [42]}, {'type': 'LineString', 'arcs': [42]}),
    ('{"type": "LineString", "arcs": [42]}', {'type': 'LineString', 'arcs': [42]}),
    ('string', ERROR),
    (1, ERROR),
    ('3.14', ERROR),
    ('', ERROR),
])
def test_cast_geojson_topojson(value, result):
    assert types.cast_geojson_topojson(value) == result
