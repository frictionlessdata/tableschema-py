# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
from tableschema import helpers
from tableschema import exceptions
from . import base


class TestHelpers(base.BaseTestCase):

    def test_load_json_source_dict(self):
        source = {
            'this': 'that',
            'other': ['thing']
        }

        self.assertTrue(helpers.load_json_source(source))

    def test_load_json_source_list(self):
        source = [
            {
                'this': 'that',
                'other': ['thing']
            }
        ]

        self.assertTrue(helpers.load_json_source(source))

    def test_load_json_source_url(self):
        source = '{0}{1}'.format(self.remote_dir, 'schema_valid_full.json')

        self.assertTrue(helpers.load_json_source(source))

    def test_load_json_source_string(self):
        source = os.path.join(self.data_dir, 'schema_valid_full.json')
        with io.open(source, mode='r+t', encoding='utf-8') as stream:
            source = stream.read()

        self.assertTrue(helpers.load_json_source(source))

    def test_load_json_source_path(self):
        source = os.path.join(self.data_dir, 'schema_valid_full.json')

        self.assertTrue(helpers.load_json_source(source))

    def test_load_json_source_invalid(self):
        source = os.path.join(self.data_dir, 'data_infer.csv')

        self.assertRaises(exceptions.InvalidJSONError,
                          helpers.load_json_source, source)
