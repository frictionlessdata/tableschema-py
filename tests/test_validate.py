# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


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


class TestValidateSchema(base.BaseTestCase):

    def test_schema_valid_simple(self):
        filepath = os.path.join(self.data_dir, 'schema_valid_simple.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertTrue(valid)

    def test_schema_valid_full(self):
        filepath = os.path.join(self.data_dir, 'schema_valid_full.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertTrue(valid)

    def test_schema_valid_pk_string(self):
        filepath = os.path.join(self.data_dir, 'schema_valid_pk_string.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertTrue(valid)

    def test_schema_valid_pk_array(self):
        filepath = os.path.join(self.data_dir, 'schema_valid_pk_array.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertTrue(valid)

    def test_schema_invalid_empty(self):
        filepath = os.path.join(self.data_dir, 'schema_invalid_empty.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertFalse(valid)

    def test_schema_invalid_wrong_type(self):
        filepath = os.path.join(self.data_dir, 'schema_invalid_wrong_type.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertFalse(valid)

    def test_schema_invalid_pk_string(self):
        filepath = os.path.join(self.data_dir, 'schema_invalid_pk_string.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertFalse(valid)

    def test_schema_invalid_pk_array(self):
        filepath = os.path.join(self.data_dir, 'schema_invalid_pk_array.json')
        with io.open(filepath) as stream:
            schema = json.load(stream)
        valid, errors = jtskit.validate(schema)
        self.assertFalse(valid)
