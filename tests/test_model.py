# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import copy
from jsontableschema import model
from jsontableschema import exceptions
from . import base


class TestModel(base.BaseTestCase):

    schema = {
        "fields": [
            {
                "name": "id",
                "type": "string",
                "constraints": {
                    "required": True,
                }
            },
            {
                "name": "height",
                "type": "number",
                "constraints": {
                    "required": False,
                }
            },
            {
                "name": "age",
                "type": "integer",
                "constraints": {
                    "required": False,
                }
            },
            {
                "name": "name",
                "type": "string",
                "constraints": {
                    "required": True,
                }
            },
            {
                "name": "occupation",
                "type": "string",
                "constraints": {
                    "required": False,
                }
            },

        ]
    }

    schema_min = {
        "fields": [
            {
                "name": "id"
            },
            {
                "name": "height"
            }
        ]
    }

    def test_headers(self):
        m = model.SchemaModel(self.schema)
        self.assertEqual(len(m.headers), 5)

    def test_required_headers(self):
        m = model.SchemaModel(self.schema)
        self.assertEqual(len(m.required_headers), 2)

    def test_has_field_true(self):
        m = model.SchemaModel(self.schema)
        self.assertTrue(m.has_field('name'))

    def test_has_field_false(self):
        m = model.SchemaModel(self.schema)
        self.assertFalse(m.has_field('religion'))

    def test_get_fields_by_type(self):

        m = model.SchemaModel(self.schema)

        self.assertEqual(len(m.get_fields_by_type('string')), 3)
        self.assertEqual(len(m.get_fields_by_type('number')), 1)
        self.assertEqual(len(m.get_fields_by_type('integer')), 1)

    def test_case_insensitive_headers(self):
        _schema = copy.deepcopy(self.schema)
        for field in _schema['fields']:
            field['name'] = field['name'].title()

        m = model.SchemaModel(_schema, case_insensitive_headers=True)
        expected = set(['id', 'height', 'name', 'age', 'occupation'])

        self.assertEqual(set(m.headers), expected)

    def test_invalid_json_raises(self):
        source = os.path.join(self.data_dir, 'data_infer.csv')

        self.assertRaises(exceptions.InvalidJSONError,
                          model.SchemaModel, source)

    def test_invalid_jts_raises(self):
        source = os.path.join(self.data_dir, 'schema_invalid_empty.json')

        self.assertRaises(exceptions.InvalidSchemaError,
                          model.SchemaModel, source)

    def test_defaults_are_set(self):
        m = model.SchemaModel(self.schema_min)
        self.assertEqual(len(m.get_fields_by_type('string')), 2)
