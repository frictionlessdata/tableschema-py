# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import pytest
from tableschema import exceptions, helpers


def test_retrieve_descriptor_dict():
    source = {'this': 'that', 'other': ['thing']}
    assert helpers.retrieve_descriptor(source)


def test_retrieve_descriptor_list():
    source = [{'this': 'that', 'other': ['thing']}]
    assert helpers.retrieve_descriptor(source)


def test_retrieve_descriptor_url():
    source = 'data/schema_valid_full.json'
    assert helpers.retrieve_descriptor(source)


def test_retrieve_descriptor_path():
    source = 'data/schema_valid_full.json'
    assert helpers.retrieve_descriptor(source)


def test_retrieve_descriptor_invalid():
    source = 'data/data_infer.csv'
    with pytest.raises(exceptions.LoadError):
        helpers.retrieve_descriptor(source)
