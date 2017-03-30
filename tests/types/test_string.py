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
    ('string', 'string'),
    ('', ''),
    (0, ERROR),
])
def test_cast_string_default(value, result):
    assert types.cast_string_default(value) == result


@pytest.mark.parametrize('value, result', [
    ('http://google.com', 'http://google.com'),
    ('string', ERROR),
    ('', ERROR),
    (0, ERROR),
])
def test_cast_string_uri(value, result):
    assert types.cast_string_uri(value) == result


@pytest.mark.parametrize('value, result', [
    ('name@gmail.com', 'name@gmail.com'),
    ('http://google.com', ERROR),
    ('string', ERROR),
    ('', ERROR),
    (0, ERROR),
])
def test_cast_string_email(value, result):
    assert types.cast_string_email(value) == result


@pytest.mark.parametrize('value, result', [
    ('dGVzdA==', 'dGVzdA=='),
    ('', ''),
    ('string', ERROR),
    (0, ERROR),
])
def test_cast_string_binary(value, result):
    assert types.cast_string_binary(value) == result
