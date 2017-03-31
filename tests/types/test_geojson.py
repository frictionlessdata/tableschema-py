# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('format, value, result', [
    ('default',
        {'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None},
        {'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None}),
    ('default',
        '{"geometry": null, "type": "Feature", "properties": {"\\u00c3": "\\u00c3"}}',
        {'properties': {'Ã': 'Ã'}, 'type': 'Feature', 'geometry': None}),
    ('default', {'coordinates': [0, 0, 0], 'type': 'Point'}, ERROR),
    ('default', 'string', ERROR),
    ('default', 1, ERROR),
    ('default', '3.14', ERROR),
    ('default', '', ERROR),
    ('default', {}, ERROR),
    ('default', '{}', ERROR),
    ('topojson',
        {'type': 'LineString', 'arcs': [42]},
        {'type': 'LineString', 'arcs': [42]}),
    ('topojson',
        '{"type": "LineString", "arcs": [42]}',
        {'type': 'LineString', 'arcs': [42]}),
    ('topojson', 'string', ERROR),
    ('topojson', 1, ERROR),
    ('topojson', '3.14', ERROR),
    ('topojson', '', ERROR),
])
def test_cast_geojson(format, value, result):
    assert types.cast_geojson(format, value) == result
