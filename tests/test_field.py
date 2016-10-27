# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import pytest
import requests
from jsontableschema import Field, exceptions


# Constants

DESCRIPTOR_MIN = {'name': 'id'}
DESCRIPTOR_MAX = {
    'name': 'id',
    'type': 'integer',
    'format': 'object',
    'constraints': {'required': True},
}


# Tests

def test_descriptor():
    assert Field(DESCRIPTOR_MIN).descriptor == DESCRIPTOR_MIN


def test_name():
    assert Field(DESCRIPTOR_MIN).name == 'id'


def test_type():
    assert Field(DESCRIPTOR_MIN).type == 'string'
    assert Field(DESCRIPTOR_MAX).type == 'integer'


def test_format():
    assert Field(DESCRIPTOR_MIN).format == 'default'
    assert Field(DESCRIPTOR_MAX).format == 'object'


def test_constraints():
    assert Field(DESCRIPTOR_MIN).constraints == {}
    assert Field(DESCRIPTOR_MAX).constraints == {'required': True}


def test_cast_value():
    # Success
    assert Field(DESCRIPTOR_MAX).cast_value('1') == 1
    # Constraint error
    with pytest.raises(exceptions.ConstraintError):
        Field(DESCRIPTOR_MAX).cast_value('')


def test_cast_value_skip_constraints():
    assert Field(DESCRIPTOR_MIN).cast_value('', skip_constraints=True) == ''


def test_test_value():
    assert Field(DESCRIPTOR_MAX).test_value('1') == True
    assert Field(DESCRIPTOR_MAX).test_value('string') == False
    assert Field(DESCRIPTOR_MAX).test_value('') == False


def test_test_value_skip_constraints():
    assert Field(DESCRIPTOR_MIN).test_value('', skip_constraints=True) == True
