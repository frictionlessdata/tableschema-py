# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from jsontableschema import types
from . import base


class TestTypes(base.BaseTestCase):

    BASE_FIELD = {
        'name': 'Name',
        'type': 'string',
        'format': 'default',
        'constraints': {
            'required': True
        }
    }

    def test_string_type_simple_true(self):

        value = 'string'
        field = self.BASE_FIELD.copy()
        _type = types.StringType(field)

        self.assertTrue(_type.cast(value))

    def test_string_type_simple_false(self):

        value = 1
        field = self.BASE_FIELD.copy()
        _type = types.StringType(field)

        self.assertFalse(_type.cast(value))

    def test_integer_type_simple_true(self):

        value = 1
        field = self.BASE_FIELD.copy()
        field['type'] = 'integer'
        _type = types.IntegerType(field)

        self.assertTrue(_type.cast(value))

    def test_integer_type_simple_false(self):

        value = 'string'
        field = self.BASE_FIELD.copy()
        field['type'] = 'integer'
        _type = types.IntegerType(field)

        self.assertFalse(_type.cast(value))

    def test_number_type_simple_true(self):

        value = '10.00'
        field = self.BASE_FIELD.copy()
        field['type'] = 'number'
        _type = types.NumberType(field)

        self.assertTrue(_type.cast(value))

    def test_number_type_simple_false(self):

        value = 'string'
        field = self.BASE_FIELD.copy()
        field['type'] = 'number'
        _type = types.NumberType(field)

        self.assertFalse(_type.cast(value))

    def test_number_type_with_currency_format_true(self):

        value1 = '10,000.00'
        value2 = '10;000.00'
        value3 = '$10000.00'
        field = self.BASE_FIELD.copy()
        field['type'] = 'number'
        field['format'] = 'currency'
        _type = types.NumberType(field)

        self.assertTrue(_type.cast(value1))
        self.assertTrue(_type.cast(value2))
        self.assertTrue(_type.cast(value3))

    def test_number_type_with_currency_format_false(self):

        value1 = '10,000a.00'
        value2 = '10+000.00'
        value3 = '$10:000.00'
        field = self.BASE_FIELD.copy()
        field['type'] = 'number'
        field['format'] = 'currency'
        _type = types.NumberType(field)

        self.assertFalse(_type.cast(value1))
        self.assertFalse(_type.cast(value2))
        self.assertFalse(_type.cast(value3))

    def test_date_type_simple_true(self):

        value = '2019-01-01'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        _type = types.DateType(field)

        self.assertTrue(_type.cast(value))

    def test_date_type_any_true(self):

        value = '10th Jan 1969'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        field['format'] = 'any'
        _type = types.DateType(field)

        self.assertTrue(_type.cast(value))

    def test_date_type_fmt_true(self):

        value = '10/06/2014'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        field['format'] = 'fmt:DD/MM/YYYY'
        _type = types.DateType(field)

        self.assertTrue(_type.cast(value))

    def test_date_type_simple_false(self):

        value = '01-01-2019'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        _type = types.DateType(field)

        self.assertFalse(_type.cast(value))

    def test_date_type_any_false(self):

        value = '10th Jan nineteen sixty nine'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        field['format'] = 'any'
        _type = types.DateType(field)

        self.assertFalse(_type.cast(value))

    def test_date_type_fmt_false(self):

        value = '2014/12/19'
        field = self.BASE_FIELD.copy()
        field['type'] = 'date'
        field['type'] = 'fmt:DD/MM/YYYY'
        _type = types.DateType(field)

        self.assertFalse(_type.cast(value))

    def test_time_type_simple_true(self):

        value = '06:00:00'
        field = self.BASE_FIELD.copy()
        field['type'] = 'time'
        _type = types.TimeType(field)

        self.assertTrue(_type.cast(value))

    def test_time_type_simple_false(self):

        value = '3 am'
        field = self.BASE_FIELD.copy()
        field['type'] = 'time'
        _type = types.TimeType(field)

        self.assertFalse(_type.cast(value))

    def test_datetime_type_simple_true(self):

        value = '2014-01-01T06:00:00Z'
        field = self.BASE_FIELD.copy()
        field['type'] = 'datetime'
        _type = types.DateTimeType(field)

        self.assertTrue(_type.cast(value))

    def test_datetime_type_any_true(self):

        value = '10th Jan 1969 9 am'
        field = self.BASE_FIELD.copy()
        field['type'] = 'datetime'
        field['format'] = 'any'
        _type = types.DateTimeType(field)

        self.assertTrue(_type.cast(value))

    def test_datetime_type_simple_false(self):

        value = 'Mon 1st Jan 2014 9 am'
        field = self.BASE_FIELD.copy()
        field['type'] = 'datetime'
        _type = types.DateTimeType(field)

        self.assertFalse(_type.cast(value))

    def test_boolean_type_simple_true(self):

        value = 'y'
        field = self.BASE_FIELD.copy()
        field['type'] = 'boolean'
        _type = types.BooleanType(field)

        self.assertTrue(_type.cast(value))

    def test_boolean_type_simple_false(self):

        value = 'n'
        field = self.BASE_FIELD.copy()
        field['type'] = 'boolean'
        _type = types.BooleanType(field)

        self.assertTrue(_type.cast(value))

    def test_null_type_simple_true(self):

        value = 'null'
        field = self.BASE_FIELD.copy()
        field['type'] = 'null'
        _type = types.NullType(field)

        self.assertTrue(_type.cast(value))

    def test_null_type_simple_false(self):

        value = 'isnull'
        field = self.BASE_FIELD.copy()
        field['type'] = 'null'
        _type = types.NullType(field)

        self.assertFalse(_type.cast(value))

    def test_array_type_simple_true(self):

        value = ['1', '2']
        field = self.BASE_FIELD.copy()
        field['type'] = 'array'
        _type = types.ArrayType(field)

        self.assertTrue(_type.cast(value))

    def test_array_type_simple_false(self):

        value = 'string, string'
        field = self.BASE_FIELD.copy()
        field['type'] = 'array'
        _type = types.ArrayType(field)

        self.assertFalse(_type.cast(value))

    def test_object_type_simple_true(self):

        value = {'key': 'value'}
        field = self.BASE_FIELD.copy()
        field['type'] = 'object'
        _type = types.ObjectType(field)

        self.assertTrue(_type.cast(value))

    def test_object_type_simple_false(self):
        value = ['boo', 'ya']
        field = self.BASE_FIELD.copy()
        field['type'] = 'object'
        _type = types.ObjectType(field)

        self.assertFalse(_type.cast(value))

    def test_geopoint_type_simple_true(self):

        value = '10.0, 21.00'
        field = self.BASE_FIELD.copy()
        field['type'] = 'geopoint'
        _type = types.GeoPointType(field)

        self.assertTrue(_type.cast(value))

    def test_geopoint_type_simple_false(self):

        value = 'this is not a geopoint'
        field = self.BASE_FIELD.copy()
        field['type'] = 'geopoint'
        _type = types.GeoPointType(field)

        self.assertFalse(_type.cast(value))

    def test_geojson_type_simple_true(self):

        value = {'type': 'Point'}
        field = self.BASE_FIELD.copy()
        field['type'] = 'geojson'
        _type = types.GeoJSONType(field)

        self.assertTrue(_type.cast(value))

    def test_geojson_type_simple_false(self):

        value = ''
        field = self.BASE_FIELD.copy()
        field['type'] = 'geojson'
        _type = types.GeoJSONType(field)

        self.assertFalse(_type.cast(value))

    def test_string_required_true(self):

        value = ''
        field = self.BASE_FIELD.copy()
        _type = types.StringType(field)

        self.assertFalse(_type.cast(value))

    def test_string_required_false(self):

        value = ''
        field = self.BASE_FIELD.copy()
        field['type'] = 'string'
        field['constraints']['required'] = False
        _type = types.StringType(field)

        self.assertEqual(_type.cast(value), value)

class TestString(base.BaseTestCase):
    BASE_FIELD = {
        'name': 'Name',
        'type': 'string',
        'format': 'default',
        'constraints': {
            'required': True
        }
    }

    def test_uri(self):
        field = self.BASE_FIELD.copy()
        field['format'] = 'uri'
        _type = types.StringType(field)

        value = 'http://test.com'
        self.assertEqual(_type.cast(value), value)

    def test_uri_failure(self):
        field = self.BASE_FIELD.copy()
        field['format'] = 'uri'
        _type = types.StringType(field)

        value = 'notauri'
        self.assertFalse(_type.cast(value))

    def test_uuid(self):
        field = self.BASE_FIELD.copy()
        field['format'] = 'uuid'
        _type = types.StringType(field)

        value = '12345678123456781234567812345678'
        self.assertEqual(_type.cast(value), value)
        value = 'urn:uuid:12345678-1234-5678-1234-567812345678'
        self.assertEqual(_type.cast(value), value)
        value = '123e4567-e89b-12d3-a456-426655440000'
        self.assertEqual(_type.cast(value), value)

    def test_uuid_failure(self):
        field = self.BASE_FIELD.copy()
        field['format'] = 'uuid'
        _type = types.StringType(field)

        value = '1234567812345678123456781234567?'
        self.assertFalse(_type.cast(value))
        value = '1234567812345678123456781234567'
        self.assertFalse(_type.cast(value))
        value = 'X23e4567-e89b-12d3-a456-426655440000'
        self.assertFalse(_type.cast(value))
