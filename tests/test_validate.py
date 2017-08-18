# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import pytest
from tableschema import validate, exceptions


def test_schema_valid_simple():
    valid = validate('data/schema_valid_simple.json')
    assert valid


def test_schema_valid_full():
    valid = validate('data/schema_valid_full.json')
    assert valid


def test_schema_valid_pk_array():
    valid = validate('data/schema_valid_pk_array.json')
    assert valid


def test_schema_invalid_empty():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_empty.json')


def test_schema_invalid_wrong_type():
    with pytest.raises(exceptions.ValidationError):
        valid = validate([])


@pytest.mark.skip('changes between specs-rc.v1 and specs-rc.v2')
def test_schema_invalid_pk_string():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_pk_string.json')


def test_schema_invalid_pk_array():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_pk_array.json')


def test_schema_valid_fk_array():
    valid = validate('data/schema_valid_fk_array.json')
    assert valid


@pytest.mark.skip('changes between specs-rc.v1 and specs-rc.v2')
def test_schema_invalid_fk_string():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_string.json')


def test_schema_invalid_fk_no_reference():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_no_reference.json')


def test_schema_invalid_fk_array():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_array.json')


def test_schema_invalid_fk_ref_is_an_array_fields_is_a_string():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_string_array_ref.json')


def test_schema_invalid_fk_reference_is_a_string_fields_is_an_array():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_array_string_ref.json')


def test_schema_invalid_fk_reference_array_number_mismatch():
    with pytest.raises(exceptions.ValidationError):
        valid = validate('data/schema_invalid_fk_array_wrong_number.json')


def test_primary_key_is_not_a_valid_type():
    with pytest.raises(exceptions.ValidationError) as excinfo:
        valid = validate('data/schema_invalid_pk_is_wrong_type.json')
    assert len(excinfo.value.errors) == 2


def test_schema_multiple_errors_no_fail_fast_true():
    with pytest.raises(exceptions.ValidationError) as excinfo:
        valid = validate('data/schema_invalid_multiple_errors.json')
    assert len(excinfo.value.errors) == 3
