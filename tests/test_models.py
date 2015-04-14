# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import copy
from jtskit import models
from jtskit import exceptions
from . import base


class TestModels(base.BaseTestCase):

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

    def test_headers(self):

        model = models.SchemaModel(self.schema)

        self.assertEqual(len(model.headers), 5)

    def test_required_headers(self):

        model = models.SchemaModel(self.schema)

        self.assertEqual(len(model.required_headers), 2)

    def test_has_field_true(self):

        model = models.SchemaModel(self.schema)

        self.assertTrue(model.has_field('name'))

    def test_has_field_false(self):

        model = models.SchemaModel(self.schema)

        self.assertFalse(model.has_field('religion'))


    def test_get_fields_by_type(self):

        model = models.SchemaModel(self.schema)

        self.assertEqual(len(model.get_fields_by_type('string')), 3)
        self.assertEqual(len(model.get_fields_by_type('number')), 1)
        self.assertEqual(len(model.get_fields_by_type('integer')), 1)

    def test_case_insensitive_headers(self):
        _schema = copy.deepcopy(self.schema)
        for field in _schema['fields']:
            field['name'] = field['name'].title()

        model = models.SchemaModel(_schema, case_insensitive_headers=True)
        expected = set(['id', 'height', 'name', 'age', 'occupation'])
        
        self.assertEqual(set(model.headers), expected)

    def test_invalid_json_raises(self):
        source = os.path.join(self.data_dir, 'data_infer.csv')

        self.assertRaises(exceptions.InvalidJSONError,
                          models.SchemaModel, source)

    def test_invalid_jts_raises(self):
        source = os.path.join(self.data_dir, 'schema_invalid_empty.json')

        self.assertRaises(exceptions.InvalidSchemaError,
                          models.SchemaModel, source)
