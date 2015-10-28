# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ast

from click.testing import CliRunner

from . import base
from jsontableschema import cli
from jsontableschema import model


class TestCliInfer(base.BaseTestCase):

    def test_infer_schema(self):
        runner = CliRunner()
        result = runner.invoke(cli.infer, ['examples/data_infer.csv'])

        # output is a string, evaluate to a dict
        schema = ast.literal_eval(result.output)

        schema_model = model.SchemaModel(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')

    def test_infer_schema_utf8(self):
        '''UTF8 encoded data containing non-ascii characters.'''
        runner = CliRunner()
        result = runner.invoke(cli.infer, ['examples/data_infer_utf8.csv'])

        # output is a string, evaluate to a dict
        schema = ast.literal_eval(result.output)

        schema_model = model.SchemaModel(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')
