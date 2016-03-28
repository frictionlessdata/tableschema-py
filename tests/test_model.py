# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import copy
from decimal import Decimal
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

    def test_fields_arent_required_by_default(self):
        schema = {
            "fields": [
                {"name": "id", "constraints": {"required": True}},
                {"name": "label"}
            ]
        }
        m = model.SchemaModel(schema)
        self.assertEqual(len(m.required_headers), 1)

    def test_schema_is_not_mutating(self):
        schema = {"fields": [{"name": "id"}]}
        schema_copy = copy.deepcopy(schema)
        model.SchemaModel(schema)
        self.assertEqual(schema, schema_copy)


class TestData(base.BaseTestCase):
    def setUp(self):
        self.schema = {
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
        super(TestData, self).setUp()

    def test_convert_row(self):
        m = model.SchemaModel(self.schema)
        converted_row = list(m.convert_row(
            'string', '10.0', '1', 'string', 'string'))
        self.assertEqual(['string', Decimal(10.0), 1, 'string', 'string'],
                         converted_row)

    def test_convert_row_null_values(self):
        m = model.SchemaModel(self.schema)
        converted_row = list(m.convert_row('string', '', '-', 'string', 'null'))
        assert ['string', None, None, 'string', None] == converted_row

    def test_convert_row_too_few_items(self):
        m = model.SchemaModel(self.schema)
        self.assertRaises(exceptions.ConversionError, list,
                          m.convert_row('string', '10.0', '1', 'string'))

    def test_convert_row_too_many_items(self):
        m = model.SchemaModel(self.schema)
        self.assertRaises(exceptions.ConversionError, list,
                          m.convert_row('string', '10.0', '1', 'string',
                                        'string', 'string', 'string',
                                        fail_fast=True))

    def test_convert_row_wrong_type_fail_fast(self):
        m = model.SchemaModel(self.schema)
        self.assertRaises(exceptions.InvalidCastError, list,
                          m.convert_row('string', 'notdecimal', '10.6',
                                        'string', 'string', fail_fast=True))

    def test_convert_row_wrong_type_multiple_errors(self):
        m = model.SchemaModel(self.schema)
        with self.assertRaises(exceptions.MultipleInvalid) as cm:
            list(m.convert_row('string', 'notdecimal', '10.6', 'string',
                               'string'))
            self.assertEquals(2, len(cm.exception.errors))

    def test_convert_rows(self):
        m = model.SchemaModel(self.schema)
        rows = m.convert([['string', '10.0', '1', 'string', 'string'],
                          ['string', '10.0', '1', 'string', 'string'],
                          ['string', '10.0', '1', 'string', 'string'],
                          ['string', '10.0', '1', 'string', 'string'],
                          ['string', '10.0', '1', 'string', 'string']])
        for row in rows:
            self.assertEqual(['string', Decimal(10.0), 1, 'string', 'string'],
                             row)

    def test_convert_rows_invalid_in_various_rows_fail_fast(self):
        m = model.SchemaModel(self.schema)
        self.assertRaises(
            exceptions.InvalidCastError,
            list,
            m.convert(
                [['string', 'not', '1', 'string', 'string'],
                 ['string', '10.0', '1', 'string', 'string'],
                 ['string', 'an', '1', 'string', 'string'],
                 ['string', '10.0', '1', 'string', 'string'],
                 ['string', '10.0', 'integer', 'string', 'string']],
                fail_fast=True)
        )

    def test_convert_rows_invalid_in_various_rows(self):
        m = model.SchemaModel(self.schema)
        with self.assertRaises(exceptions.MultipleInvalid) as cm:
            list(m.convert([['string', 'not', '1', 'string', 'string'],
                            ['string', '10.0', '1', 'string', 'string'],
                            ['string', 'an', '1', 'string', 'string'],
                            ['string', '10.0', '1', 'string', 'string'],
                            ['string', '10.0', 'integer', 'string', 'string']])
                 )
            self.assertEquals(3, len(cm.errors))

    def test_convert_rows_invalid_varying_length_rows(self):
        m = model.SchemaModel(self.schema)
        with self.assertRaises(exceptions.MultipleInvalid) as cm:
            list(m.convert([['string', '10.0', '1', 'string'],
                            ['string', '10.0', '1', 'string', 'string'],
                            ['string', '10.0', '1', 'string', 'string', 1],
                            ['string', '10.0', '1', 'string', 'string'],
                            ['string', '10.0', '1', 'string', 'string']])
                 )
            self.assertEquals(2, len(cm.errors))

    def test_convert_rows_invalid_varying_length_rows_fail_fast(self):
        m = model.SchemaModel(self.schema)
        self.assertRaises(
            exceptions.ConversionError,
            list,
            m.convert([['string', '10.0', '1', 'string'],
                       ['string', '10.0', '1', 'string', 'string'],
                       ['string', '10.0', '1', 'string', 'string', 1],
                       ['string', '10.0', '1', 'string', 'string'],
                       ['string', '10.0', '1', 'string', 'string']],
                      fail_fast=True)
        )
