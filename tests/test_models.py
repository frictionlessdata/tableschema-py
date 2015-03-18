# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from jtskit import models
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

        model = models.JSONTableSchema(self.schema)

        self.assertEqual(len(model.headers), 5)

    def test_required_headers(self):

        model = models.JSONTableSchema(self.schema)

        self.assertEqual(len(model.required_headers), 2)

    def test_has_field_true(self):

        model = models.JSONTableSchema(self.schema)

        self.assertTrue(model.has_field('name'))


    def test_has_field_false(self):

        model = models.JSONTableSchema(self.schema)

        self.assertFalse(model.has_field('religion'))


    def test_get_fields_by_type(self):

        model = models.JSONTableSchema(self.schema)

        self.assertEqual(len(model.get_fields_by_type('string')), 3)
        self.assertEqual(len(model.get_fields_by_type('number')), 1)
        self.assertEqual(len(model.get_fields_by_type('integer')), 1)
