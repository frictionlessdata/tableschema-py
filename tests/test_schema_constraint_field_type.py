# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import json
import os

import pytest

from tableschema import Schema, exceptions, validate

# Tests on built-in constraints - field type consistency

CONSTRAINT_FIELDTYPE_TESTCASES = [
    # minLength constraint (applies to collections (string, array, object))
    ('minLength', {'minLength': 4}, None, True),
    ('minLength', {'minLength': 4}, 'any', False),
    ('minLength', {'minLength': 4}, 'array', True),
    ('minLength', {'minLength': 4}, 'boolean', False),
    ('minLength', {'minLength': 4}, 'date', False),
    ('minLength', {'minLength': 4}, 'datetime', False),
    ('minLength', {'minLength': 4}, 'duration', False),
    ('minLength', {'minLength': 4}, 'geojson', False),
    ('minLength', {'minLength': 4}, 'geopoint', False),
    ('minLength', {'minLength': 4}, 'integer', False),
    ('minLength', {'minLength': 4}, 'number', False),
    ('minLength', {'minLength': 4}, 'object', True),
    ('minLength', {'minLength': 4}, 'string', True),
    ('minLength', {'minLength': 4}, 'time', False),
    ('minLength', {'minLength': 4}, 'year', False),
    ('minLength', {'minLength': 4}, 'yearmonth', False),

    # maxLength constraint (applies to collections (string, array, object))
    ('maxLength', {'maxLength': 3}, None, True),
    ('maxLength', {'maxLength': 3}, 'any', False),
    ('maxLength', {'maxLength': 3}, 'array', True),
    ('maxLength', {'maxLength': 3}, 'boolean', False),
    ('maxLength', {'maxLength': 3}, 'date', False),
    ('maxLength', {'maxLength': 3}, 'datetime', False),
    ('maxLength', {'maxLength': 3}, 'duration', False),
    ('maxLength', {'maxLength': 3}, 'geojson', False),
    ('maxLength', {'maxLength': 3}, 'geopoint', False),
    ('maxLength', {'maxLength': 3}, 'integer', False),
    ('maxLength', {'maxLength': 3}, 'number', False),
    ('maxLength', {'maxLength': 3}, 'object', True),
    ('maxLength', {'maxLength': 3}, 'string', True),
    ('maxLength', {'maxLength': 3}, 'time', False),
    ('maxLength', {'maxLength': 3}, 'year', False),
    ('maxLength', {'maxLength': 3}, 'yearmonth', False),

    # minimum constraint (applies to integer, number, date, time, datetime, year, yearmonth)
    ('minimum', {'minimum': 4}, None, False),
    ('minimum', {'minimum': 4}, 'any', False),
    ('minimum', {'minimum': 4}, 'array', False),
    ('minimum', {'minimum': 4}, 'boolean', False),
    ('minimum', {'minimum': "1789-07-14"}, 'date', True),
    ('minimum', {'minimum': "1789-07-14T08:00:00Z"}, 'datetime', True),
    ('minimum', {'minimum': 4}, 'duration', False),
    ('minimum', {'minimum': 4}, 'geojson', False),
    ('minimum', {'minimum': 4}, 'geopoint', False),
    ('minimum', {'minimum': 4}, 'integer', True),
    ('minimum', {'minimum': 4}, 'number', True),
    ('minimum', {'minimum': 4}, 'object', False),
    ('minimum', {'minimum': 4}, 'string', False),
    ('minimum', {'minimum': "07:07:07"}, 'time', True),
    ('minimum', {'minimum': 4}, 'year', True),
    ('minimum', {'minimum': "1789-07"}, 'yearmonth', True),

    # maximum constraint (applies to integer, number, date, time and datetime, year, yearmonth)
    ('maximum', {'maximum': 4}, None, False),
    ('maximum', {'maximum': 4}, 'any', False),
    ('maximum', {'maximum': 4}, 'array', False),
    ('maximum', {'maximum': 4}, 'boolean', False),
    ('maximum', {'maximum': "2001-01-01"}, 'date', True),
    ('maximum', {'maximum': "2001-01-01T12:00:00Z"}, 'datetime', True),
    ('maximum', {'maximum': 4}, 'duration', False),
    ('maximum', {'maximum': 4}, 'geojson', False),
    ('maximum', {'maximum': 4}, 'geopoint', False),
    ('maximum', {'maximum': 4}, 'integer', True),
    ('maximum', {'maximum': 4}, 'number', True),
    ('maximum', {'maximum': 4}, 'object', False),
    ('maximum', {'maximum': 4}, 'string', False),
    ('maximum', {'maximum': "08:09:10"}, 'time', True),
    ('maximum', {'maximum': 4}, 'year', True),
    ('maximum', {'maximum': "2001-01"}, 'yearmonth', True),

    # pattern constraint (apply to string)
    ('pattern', {'pattern': '[0-9]+'}, None, True),
    ('pattern', {'pattern': '[0-9]+'}, 'any', False),
    ('pattern', {'pattern': '[0-9]+'}, 'array', False),
    ('pattern', {'pattern': '[0-9]+'}, 'boolean', False),
    ('pattern', {'pattern': '[0-9]+'}, 'date', False),
    ('pattern', {'pattern': '[0-9]+'}, 'datetime', False),
    ('pattern', {'pattern': '[0-9]+'}, 'duration', False),
    ('pattern', {'pattern': '[0-9]+'}, 'geojson', False),
    ('pattern', {'pattern': '[0-9]+'}, 'geopoint', False),
    ('pattern', {'pattern': '[0-9]+'}, 'integer', False),
    ('pattern', {'pattern': '[0-9]+'}, 'number', False),
    ('pattern', {'pattern': '[0-9]+'}, 'object', False),
    ('pattern', {'pattern': '[0-9]+'}, 'string', True),
    ('pattern', {'pattern': '[0-9]+'}, 'time', False),
    ('pattern', {'pattern': '[0-9]+'}, 'year', False),
    ('pattern', {'pattern': '[0-9]+'}, 'yearmonth', False)
]


@pytest.mark.parametrize("constraint_name, constraint, field_type, expected", CONSTRAINT_FIELDTYPE_TESTCASES)
def test_schema_constraint_field_type(constraint_name, constraint, field_type, expected):
    field = {
        'name': 'f',
        'constraints': constraint,
    }
    if field_type is not None:
        field['type'] = field_type
    test_descriptor = {'fields': [field]}

    message = 'constraint "{}" can{} be applied to "{}" field' \
        .format(constraint_name, "" if expected else "not",
                "default" if field_type is None else field_type)

    table_schema = Schema(descriptor=test_descriptor)
    assert table_schema.valid == expected, message
