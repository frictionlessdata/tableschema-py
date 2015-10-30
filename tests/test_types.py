# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, date, time
from decimal import Decimal

from jsontableschema import types, exceptions

from . import base


class TestString(base.BaseTestCase):
    def setUp(self):
        super(TestString, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'string',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_string_type_simple_true(self):
        _type = types.StringType(self.field)
        value = 'a string'
        self.assertEquals(_type.cast(value), value)

        value = u'a string'
        self.assertEquals(_type.cast(value), value)

    def test_string_type_simple_false(self):
        _type = types.StringType(self.field)

        value = 1
        self.assertRaises(exceptions.InvalidCastError, _type.cast, value)

    def test_valid_email(self):
        self.field['format'] = 'email'
        _type = types.StringType(self.field)
        value = 'test@test.com'
        self.assertEquals(_type.cast(value), value)

        value = 'customer/department=shipping@example.com'
        self.assertEquals(_type.cast(value), value)

        value = '\$A12345@example.com'
        self.assertEquals(_type.cast(value), value)

        value = '!def!xyz%abc@example.com'
        self.assertEquals(_type.cast(value), value)

    def test_invalid_email_fails(self):
        self.field['format'] = 'email'
        _type = types.StringType(self.field)

        value = 1
        self.assertRaises(exceptions.InvalidCastError, _type.cast, value)

        value = 'notanemail'
        self.assertRaises(exceptions.InvalidEmail, _type.cast, value)

    def test_uri(self):
        self.field['format'] = 'uri'
        _type = types.StringType(self.field)

        value = 'http://test.com'
        self.assertEqual(_type.cast(value), value)

    def test_uri_failure(self):
        self.field['format'] = 'uri'
        _type = types.StringType(self.field)

        value = 'notauri'
        self.assertRaises(exceptions.InvalidURI, _type.cast, value)

    def test_uuid(self):
        self.field['format'] = 'uuid'
        _type = types.StringType(self.field)

        value = '12345678123456781234567812345678'
        self.assertEqual(_type.cast(value), value)
        value = 'urn:uuid:12345678-1234-5678-1234-567812345678'
        self.assertEqual(_type.cast(value), value)
        value = '123e4567-e89b-12d3-a456-426655440000'
        self.assertEqual(_type.cast(value), value)

    def test_uuid_failure(self):
        self.field['format'] = 'uuid'
        _type = types.StringType(self.field)

        value = '1234567812345678123456781234567?'
        self.assertRaises(exceptions.InvalidUUID, _type.cast, value)
        value = '1234567812345678123456781234567'
        self.assertRaises(exceptions.InvalidUUID, _type.cast, value)
        value = 'X23e4567-e89b-12d3-a456-426655440000'
        self.assertRaises(exceptions.InvalidUUID, _type.cast, value)


class TestNumber(base.BaseTestCase):
    def setUp(self):
        super(TestNumber, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'number',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_number_type_simple_true(self):
        value = '10.00'
        _type = types.NumberType(self.field)

        self.assertEquals(_type.cast(value), Decimal(value))

    def test_number_type_simple_false(self):
        value = 'string'
        _type = types.NumberType(self.field)

        self.assertRaises(exceptions.InvalidCastError, _type.cast, value)

    def test_number_type_with_currency_format_true(self):
        value1 = '10,000.00'
        value2 = '10;000.00'
        value3 = '$10000.00'
        self.field['format'] = 'currency'
        _type = types.NumberType(self.field)

        self.assertTrue(_type.cast(value1))
        self.assertTrue(_type.cast(value2))
        self.assertTrue(_type.cast(value3))

        value = '$10, 000.00'
        self.assertTrue(_type.cast(value))

        value = '£10 000.00'
        self.assertTrue(_type.cast(value))

    def test_number_type_with_currency_format_false(self):
        value1 = '10,000a.00'
        value2 = '10+000.00'
        value3 = '$10:000.00'
        self.field['format'] = 'currency'
        _type = types.NumberType(self.field)

        self.assertRaises(exceptions.InvalidCastError, _type.cast, value1)
        self.assertRaises(exceptions.InvalidCastError, _type.cast, value2)
        self.assertRaises(exceptions.InvalidCastError, _type.cast, value3)


class TestInteger(base.BaseTestCase):
    def setUp(self):
        super(TestInteger, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'integer',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_integer_type_simple(self):
        value = 1
        _type = types.IntegerType(self.field)

        self.assertEquals(_type.cast(value), value)

    def test_integer_type_simple_raises(self):
        value = 'string'
        _type = types.IntegerType(self.field)

        self.assertRaises(exceptions.InvalidCastError, _type.cast, value)


class TestBoolean(base.BaseTestCase):
    def setUp(self):
        super(TestBoolean, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'boolean',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_boolean_type_simple_true(self):
        value = 'y'
        _type = types.BooleanType(self.field)

        self.assertTrue(_type.cast(value))

    def test_boolean_type_simple_false(self):
        value = 'n'
        _type = types.BooleanType(self.field)

        self.assertFalse(_type.cast(value))

    def test_yes_no(self):
        _type = types.BooleanType(self.field)

        value = 'yes'
        self.assertTrue(_type.cast(value))
        value = 'no'
        self.assertFalse(_type.cast(value))

    def test_one_or_zero(self):
        _type = types.BooleanType(self.field)

        value = '1'
        self.assertTrue(_type.cast(value))
        value = '0'
        self.assertFalse(_type.cast(value))

        value = 1
        self.assertTrue(_type.cast(value))
        value = 0
        self.assertFalse(_type.cast(value))

    def test_t_or_f(self):
        _type = types.BooleanType(self.field)

        value = 't'
        self.assertTrue(_type.cast(value))
        value = 'f'
        self.assertFalse(_type.cast(value))

    def test_true_or_false(self):
        _type = types.BooleanType(self.field)

        value = 'true'
        self.assertTrue(_type.cast(value))
        value = 'false'
        self.assertFalse(_type.cast(value))

    def test_invalid_boolean_value_fails(self):
        _type = types.BooleanType(self.field)

        value = 'not a true value'
        self.assertRaises(exceptions.InvalidBooleanType, _type.cast, value)
        value = 11231902333
        self.assertRaises(exceptions.InvalidBooleanType, _type.cast, value)


class TestNull(base.BaseTestCase):
    def setUp(self):
        super(TestNull, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'null',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_null_type_simple_true(self):
        _type = types.NullType(self.field)

        value = 'null'
        self.assertIs(None, _type.cast(value))

        value = 'null'
        self.assertIs(None, _type.cast(value))

        value = 'none'
        self.assertIs(None, _type.cast(value))

        value = 'nil'
        self.assertIs(None, _type.cast(value))

        value = 'nan'
        self.assertIs(None, _type.cast(value))

        value = '-'
        self.assertIs(None, _type.cast(value))

        # spec says '' is considered missing, but '' is a valid null type
        # value = ''
        # self.assertIs(None, _type.cast(value))

    def test_null_type_simple_false(self):
        value = 'isnull'
        _type = types.NullType(self.field)

        self.assertRaises(exceptions.InvalidNoneType, _type.cast, value)


class TestObject(base.BaseTestCase):
    def setUp(self):
        super(TestObject, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'object',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_dict(self):
        value = {'key': 'value'}
        _type = types.ObjectType(self.field)

        self.assertDictEqual(_type.cast(value), value)

    def test_json_string(self):
        value = '{"key": "value"}'
        _type = types.ObjectType(self.field)

        self.assertDictEqual(_type.cast(value), {'key': 'value'})

    def test_invalid(self):
        value = ['boo', 'ya']
        _type = types.ObjectType(self.field)

        self.assertRaises(exceptions.InvalidObjectType, _type.cast, value)


class TestArray(base.BaseTestCase):
    def setUp(self):
        super(TestArray, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'array',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_array_type_simple_true(self):
        value = ['1', '2']
        _type = types.ArrayType(self.field)
        self.assertEquals(_type.cast(value), value)

    def test_array_type_simple_json_string(self):
        value = '["1", "2"]'
        _type = types.ArrayType(self.field)
        self.assertEquals(_type.cast(value), [u'1', u'2'])

    def test_array_type_simple_false(self):
        value = 'string, string'
        _type = types.ArrayType(self.field)
        self.assertRaises(exceptions.InvalidArrayType, _type.cast, value)


class TestDate(base.BaseTestCase):
    def setUp(self):
        super(TestDate, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'date',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_date_from_string_iso_format(self):
        value = '2019-01-01'
        _type = types.DateType(self.field)

        self.assertEquals(_type.cast(value), date(2019, 1, 1))

    def test_date_type_any_true(self):
        value = '10th Jan 1969'
        self.field['format'] = 'any'
        _type = types.DateType(self.field)

        self.assertEquals(_type.cast(value), date(1969, 1, 10))

    def test_date_type_fmt(self):

        value = '10/06/2014'
        self.field['format'] = 'fmt:%d/%m/%Y'
        _type = types.DateType(self.field)

        self.assertEquals(_type.cast(value), date(2014, 6, 10))

    def test_non_iso_date_fails_for_default(self):
        value = '01-01-2019'
        _type = types.DateType(self.field)

        self.assertRaises(exceptions.InvalidDateType, _type.cast, value)

    def test_date_type_any_parser_fail(self):
        value = '10th Jan nineteen sixty nine'
        self.field['format'] = 'any'
        _type = types.DateType(self.field)

        self.assertRaises(exceptions.InvalidDateType, _type.cast, value)

    def test_invalid_fmt(self):
        value = '2014/12/19'
        self.field['type'] = 'fmt:DD/MM/YYYY'
        _type = types.DateType(self.field)

        self.assertRaises(exceptions.InvalidDateType, _type.cast, value)

    def test_valid_fmt_invalid_value(self):
        value = '2014/12/19'
        self.field['type'] = 'fmt:%m/%d/%y'
        _type = types.DateType(self.field)

        self.assertRaises(exceptions.InvalidDateType, _type.cast, value)


class TestTime(base.BaseTestCase):
    def setUp(self):
        super(TestTime, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'time',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_time_type_default(self):
        value = '06:00:00'
        _type = types.TimeType(self.field)
        self.assertEquals(_type.cast(value), time(6))

    def test_time_type_non_iso_raises_error(self):
        value = '3 am'
        _type = types.TimeType(self.field)
        self.assertRaises(exceptions.InvalidTimeType, _type.cast, value)

    def test_time_type_parsing(self):
        value = '3:00 am'
        self.field['format'] = 'any'
        _type = types.TimeType(self.field)
        self.assertEquals(_type.cast(value), time(3))

    def test_time_type_format(self):
        value = '3:00'
        self.field['format'] = 'fmt:%H:%M'
        _type = types.TimeType(self.field)
        self.assertEquals(_type.cast(value), time(3))

    def test_time_invalid_type_format(self):
        value = 3.00
        self.field['format'] = 'fmt:%H:%M'
        _type = types.TimeType(self.field)
        self.assertRaises(exceptions.InvalidTimeType, _type.cast, value)

        value = {}
        _type = types.TimeType(self.field)
        self.assertRaises(exceptions.InvalidTimeType, _type.cast, value)

        value = []
        _type = types.TimeType(self.field)
        self.assertRaises(exceptions.InvalidTimeType, _type.cast, value)


class TestDateTime(base.BaseTestCase):
    def setUp(self):
        super(TestDateTime, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'datetime',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_valid_iso_datetime(self):
        value = '2014-01-01T06:00:00Z'
        _type = types.DateTimeType(self.field)
        self.assertEquals(_type.cast(value), datetime(2014, 1, 1, 6))

    def test_any_parser_guessing(self):
        value = '10th Jan 1969 9 am'
        self.field['format'] = 'any'
        _type = types.DateTimeType(self.field)
        self.assertEquals(_type.cast(value), datetime(1969, 1, 10, 9))

    def test_specified_format(self):
        value = '21/11/06 16:30'
        self.field['format'] = 'fmt:%d/%m/%y %H:%M'
        _type = types.DateTimeType(self.field)
        self.assertEquals(_type.cast(value), datetime(2006, 11, 21, 16, 30))

    def test_non_iso_datetime_fails_for_default(self):
        value = 'Mon 1st Jan 2014 9 am'
        _type = types.DateTimeType(self.field)
        self.assertRaises(exceptions.InvalidDateTimeType, _type.cast, value)

    def test_unparsable_date_raises_exception(self):
        value = 'the land before time'
        self.field['format'] = 'any'
        _type = types.DateTimeType(self.field)
        self.assertRaises(exceptions.InvalidDateTimeType, _type.cast, value)

    def test_invalid_date_format(self):
        value = '21/11/06 16:30'
        self.field['format'] = 'fmt:notavalidformat'
        _type = types.DateTimeType(self.field)
        self.assertRaises(exceptions.InvalidDateTimeType, _type.cast, value)


class TestGeoPoint(base.BaseTestCase):
    def setUp(self):
        super(TestGeoPoint, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'geopoint',
            'format': 'default',
            'constraints': {
                'required': True
            }
        }

    def test_geopoint_type_simple_true(self):
        value = '10.0, 21.00'
        _type = types.GeoPointType(self.field)
        self.assertEquals(_type.cast(value), [Decimal(10.0), Decimal(21)])

    def test_values_outside_longitude_range(self):
        value = '310.0, 921.00'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, value)

    def test_values_outside_latitude_range(self):
        value = '10.0, 921.00'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, value)

    def test_geopoint_type_simple_false(self):
        value = 'this is not a geopoint'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, value)

    def test_non_decimal_values(self):
        value = 'blah, blah'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, value)

    def test_wrong_length_of_points(self):
        value = '10.0, 21.00, 1'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, value)

    def test_array(self):
        self.field['format'] = 'array'
        _type = types.GeoPointType(self.field)
        self.assertEquals(_type.cast('[10.0, 21.00]'),
                          [Decimal(10.0), Decimal(21)])
        self.assertEquals(_type.cast('["10.0", "21.00"]'),
                          [Decimal(10.0), Decimal(21)])

    def test_array_invalid(self):
        self.field['format'] = 'array'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, ' ')
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast,
                          '["a", "b"]')
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast,
                          '[1, 2, 3]')

    def test_object(self):
        self.field['format'] = 'object'
        _type = types.GeoPointType(self.field)
        self.assertEquals(_type.cast('{"longitude": 10.0, "latitude": 21.00}'),
                          [Decimal(10.0), Decimal(21)])
        self.assertEquals(
            _type.cast('{"longitude": "10.0", "latitude": "21.00"}'),
            [Decimal(10.0), Decimal(21)]
        )

    def test_array_object(self):
        self.field['format'] = 'object'
        _type = types.GeoPointType(self.field)
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast, '[ ')
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast,
                          '{"blah": "10.0", "latitude": "21.00"}')
        self.assertRaises(exceptions.InvalidGeoPointType, _type.cast,
                          '{"longitude": "a", "latitude": "21.00"}')


class TestGeoJson(base.BaseTestCase):
    def setUp(self):
        super(TestGeoJson, self).setUp()
        self.field = {
            'name': 'Name',
            'type': 'geojson',
            'format': 'default',
            'constraints': {
                'required': False
            }
        }

    def test_geojson_type(self):
        value = {'coordinates': [0, 0, 0], 'type': 'Point'}
        self.field['type'] = 'geojson'
        _type = types.GeoJSONType(self.field)

        self.assertRaises(exceptions.InvalidGeoJSONType, _type.cast, value)

    def test_geojson_type_simple_true(self):
        value = {
            "properties": {
                "Ã": "Ã"
            },
            "type": "Feature",
            "geometry": None,
        }

        self.field['type'] = 'geojson'
        _type = types.GeoJSONType(self.field)

        self.assertEquals(_type.cast(value), value)

    def test_geojson_type_cast_from_string(self):
        value = '{"geometry": null, "type": "Feature", "properties": {"\\u00c3": "\\u00c3"}}'
        self.field['type'] = 'geojson'
        _type = types.GeoJSONType(self.field)

        self.assertEquals(_type.cast(value), {
            "properties": {
                "Ã": "Ã"
            },
            "type": "Feature",
            "geometry": None,
        })

    def test_geojson_type_simple_false(self):
        value = ''
        self.field['type'] = 'geojson'
        _type = types.GeoJSONType(self.field)

        self.assertRaises(exceptions.InvalidGeoJSONType, _type.cast, value)
