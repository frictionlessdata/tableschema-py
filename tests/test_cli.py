# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import ast
from click.testing import CliRunner
from . import base
from tableschema import Schema, cli
os.environ['LC_ALL'] = 'en_US.UTF-8'


class TestCliInfer(base.BaseTestCase):

    def test_infer_schema(self):
        runner = CliRunner()
        result = runner.invoke(cli.infer, ['data/data_infer.csv'])

        # output is a string, evaluate to a dict
        schema = ast.literal_eval(result.output)

        schema_model = Schema(schema)

        self.assertEqual(schema_model.get_field('id').type, 'integer')
        self.assertEqual(schema_model.get_field('age').type, 'integer')
        self.assertEqual(schema_model.get_field('name').type, 'string')

    def test_infer_schema_utf8(self):
        '''UTF8 encoded data containing non-ascii characters.'''
        runner = CliRunner()
        result = runner.invoke(cli.infer, ['data/data_infer_utf8.csv'])
        # output is a string, evaluate to a dict
        schema = ast.literal_eval(result.output)

        schema_model = Schema(schema)

        self.assertEqual(schema_model.get_field('id').type, 'integer')
        self.assertEqual(schema_model.get_field('age').type, 'integer')
        self.assertEqual(schema_model.get_field('name').type, 'string')

    def test_infer_schema_greek(self):
        '''iso-8859-7 (greek) encoded data containing non-ascii characters.'''
        runner = CliRunner()
        result = runner.invoke(cli.infer,
                               ['data/data_infer_iso-8859-7.csv',
                                '--encoding=iso-8859-7'])

        # output is a string, evaluate to a dict
        schema = ast.literal_eval(result.output)

        schema_model = Schema(schema)

        self.assertEqual(schema_model.get_field('id').type, 'integer')
        self.assertEqual(schema_model.get_field('age').type, 'integer')
        self.assertEqual(schema_model.get_field('name').type, 'string')

    def test_infer_schema_greek_no_encoding_defined(self):
        '''iso-8859-7 (greek) encoded data containing non-ascii characters,
        with no encoding arg passed returns an error message.'''
        runner = CliRunner()
        result = runner.invoke(cli.infer,
                               ['data/data_infer_iso-8859-7.csv'])

        # There's an exception in the result
        self.assertTrue("Could not decode the data file as utf-8. "
                        "Please specify an encoding to use with the "
                        "--encoding argument." in result.output,)
