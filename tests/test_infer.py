# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import jsontableschema
from . import base


class TestInferSchema(base.BaseTestCase):

    def test_infer_schema(self):
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values)
        schema_model = jsontableschema.model.SchemaModel(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')

    def test_infer_schema_row_limit(self):
        filepath = os.path.join(self.data_dir, 'data_infer_row_limit.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values, row_limit=4)
        schema_model = jsontableschema.model.SchemaModel(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')

    def test_infer_schema_primary_key_string(self):
        primary_key = 'id'
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values, primary_key=primary_key)
        schema_model = jsontableschema.model.SchemaModel(schema)

        self.assertTrue(schema_model.primaryKey, primary_key)

    def test_infer_schema_primary_key_list(self):
        primary_key = ['id', 'age']
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values, primary_key=primary_key)
        schema_model = jsontableschema.model.SchemaModel(schema)

        self.assertTrue(schema_model.primaryKey, primary_key)

    def test_infer_explicit_false(self):
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values, explicit=False)

        self.assertIsNone(schema['fields'][0].get('constraints'))

    def test_infer_explicit_true(self):
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
            schema = jsontableschema.infer(headers, values, explicit=True)

        self.assertTrue(schema['fields'][0].get('constraints'))
