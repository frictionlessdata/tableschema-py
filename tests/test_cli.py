# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import ast
import pytest
from click.testing import CliRunner
from tableschema import Schema
from tableschema.cli import infer, validate
os.environ['LC_ALL'] = 'en_US.UTF-8'


# Tests

def test_infer_schema():
    runner = CliRunner()
    result = runner.invoke(infer, ['data/data_infer.csv'])
    # output is a string, evaluate to a dict
    schema = ast.literal_eval(result.output)
    schema_model = Schema(schema)
    assert schema_model.get_field('id').type == 'integer'
    assert schema_model.get_field('age').type == 'integer'
    assert schema_model.get_field('name').type == 'string'


def test_infer_schema_utf8():
    """UTF8 encoded data containing non-ascii characters."""
    runner = CliRunner()
    result = runner.invoke(infer, ['data/data_infer_utf8.csv'])
    # output is a string, evaluate to a dict
    schema = ast.literal_eval(result.output)
    schema_model = Schema(schema)
    assert schema_model.get_field('id').type == 'integer'
    assert schema_model.get_field('age').type == 'integer'
    assert schema_model.get_field('name').type == 'string'


def test_infer_schema_greek():
    """iso-8859-7 (greek) encoded data containing non-ascii characters."""
    runner = CliRunner()
    result = runner.invoke(infer,
                           ['data/data_infer_iso-8859-7.csv',
                            '--encoding=iso-8859-7'])
    # output is a string, evaluate to a dict
    schema = ast.literal_eval(result.output)
    schema_model = Schema(schema)
    assert schema_model.get_field('id').type == 'integer'
    assert schema_model.get_field('age').type == 'integer'
    assert schema_model.get_field('name').type == 'string'

def test_validate_schema():
    runner = CliRunner()
    result = runner.invoke(validate, ['data/schema_valid_simple.json'])
    assert result.output.splitlines()[0] == 'Schema is valid'
    assert result.exit_code == 0
    result = runner.invoke(validate, ['data/schema_invalid_pk_no_fields.json'])
    assert result.output.splitlines()[0] == 'Schema is not valid'
    assert result.exit_code == 1


@pytest.mark.skip
def test_infer_schema_greek_no_encoding_defined():
    """iso-8859-7 (greek) encoded data containing non-ascii characters,
    with no encoding arg passed returns an error message."""
    runner = CliRunner()
    result = runner.invoke(cli.infer, ['data/data_infer_iso-8859-7.csv'])
    # There's an exception in the result
    assert 'Could not decode the data file as utf-8.' in result.output
