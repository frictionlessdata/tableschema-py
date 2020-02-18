# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
from tableschema import infer


# Tests

def test_infer_schema():
    descriptor = infer('data/data_infer.csv')
    assert descriptor == {
        'fields': [
            {'name': 'id', 'type': 'integer', 'format': 'default'},
            {'name': 'age', 'type': 'integer', 'format': 'default'},
            {'name': 'name', 'type': 'string', 'format': 'default'}],
        'missingValues': [''],
    }


def test_infer_schema_utf8():
    descriptor = infer('data/data_infer_utf8.csv')
    assert descriptor == {
        'fields': [
            {'name': 'id', 'type': 'integer', 'format': 'default'},
            {'name': 'age', 'type': 'integer', 'format': 'default'},
            {'name': 'name', 'type': 'string', 'format': 'default'}],
        'missingValues': [''],
    }


def test_infer_schema_with_row_limit():
    descriptor = infer('data/data_infer_row_limit.csv', limit=4)
    assert descriptor == {
        'fields': [
            {'name': 'id', 'type': 'integer', 'format': 'default'},
            {'name': 'age', 'type': 'integer', 'format': 'default'},
            {'name': 'name', 'type': 'string', 'format': 'default'}],
        'missingValues': [''],
    }


def test_infer_schema_with_missing_values_default():
    descriptor = infer('data/data_infer_missing_values.csv')
    assert descriptor == {
        'fields': [
            {'name': 'id', 'type': 'string', 'format': 'default'},
            {'name': 'age', 'type': 'integer', 'format': 'default'},
            {'name': 'name', 'type': 'string', 'format': 'default'}],
        'missingValues': [''],
    }


def test_infer_schema_with_missing_values_using_the_argument():
    descriptor = infer('data/data_infer_missing_values.csv', missing_values=['-'])
    assert descriptor == {
        'fields': [
            {'name': 'id', 'type': 'integer', 'format': 'default'},
            {'name': 'age', 'type': 'integer', 'format': 'default'},
            {'name': 'name', 'type': 'string', 'format': 'default'}],
        'missingValues': ['-'],
    }


def test_check_type_boolean_string_tie():
    descriptor = infer([['f'], ['stringish']], headers=['field'])
    assert descriptor['fields'][0]['type'] == 'string'
