# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import jtskit
from . import base


class TestInferSchema(base.BaseTestCase):

    def test_infer_schema(self):
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jtskit.compat.csv_reader(stream)
            schema = jtskit.infer(headers, values)
        schema_model = jtskit.models.JSONTableSchema(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')

    def test_infer_schema_row_limit(self):
        filepath = os.path.join(self.data_dir, 'data_infer_row_limit.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jtskit.compat.csv_reader(stream)
            schema = jtskit.infer(headers, values, row_limit=4)
        schema_model = jtskit.models.JSONTableSchema(schema)

        self.assertEqual(schema_model.get_field('id')['type'], 'integer')
        self.assertEqual(schema_model.get_field('age')['type'], 'integer')
        self.assertEqual(schema_model.get_field('name')['type'], 'string')

    def test_infer_schema_primary_key_string(self):
        primary_key = 'id'
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jtskit.compat.csv_reader(stream)
            schema = jtskit.infer(headers, values, primary_key=primary_key)
        schema_model = jtskit.models.JSONTableSchema(schema)

        self.assertTrue(schema_model.primaryKey, primary_key)

    def test_infer_schema_primary_key_list(self):
        primary_key = ['id', 'age']
        filepath = os.path.join(self.data_dir, 'data_infer.csv')
        with io.open(filepath) as stream:
            headers = stream.readline().rstrip('\n').split(',')
            values = jtskit.compat.csv_reader(stream)
            schema = jtskit.infer(headers, values, primary_key=primary_key)
        schema_model = jtskit.models.JSONTableSchema(schema)

        self.assertTrue(schema_model.primaryKey, primary_key)
