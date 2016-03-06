# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import pytest
import unittest
from mock import MagicMock, patch, mock_open, call, ANY
from importlib import import_module
module = import_module('jsontableschema.resource')


class Test_export_resource(unittest.TestCase):

    # Helpers

    def setUp(self):
        self.addCleanup(patch.stopall)
        self.csv = patch.object(module, 'csv').start()
        self.json = patch.object(module, 'json').start()
        self.topen = patch.object(module, 'topen').start()
        self.open = patch.object(module.io, 'open').start()
        self.ensure_dir = patch.object(module.utilities, 'ensure_dir').start()
        self.SchemaModel = patch.object(module, 'SchemaModel').start()
        self.import_module = patch.object(module, 'import_module').start()
        self.storage = self.import_module.return_value.Storage.return_value
        self.backend_options = {'prefix': 'prefix_'}

    # Tests

    def test_export_resource(self):

        # Call function
        module.export_resource(
            table='table', schema='schema', data='data',
            backend='backend', **self.backend_options)

        # Assert calls
        self.import_module.assert_called_with('jsontableschema.plugins.backend')
        self.import_module.return_value.Storage.assert_called_with(**self.backend_options)
        self.SchemaModel.assert_called_with('schema')
        self.storage.check.assert_called_with('table')
        self.storage.create.assert_called_with(
                'table', self.SchemaModel.return_value.as_python)
        self.topen.assert_called_with('data', with_headers=True)
        self.storage.write.assert_called_with(
                'table', self.topen.return_value.__enter__.return_value)


    def test_import_resource(self):

        # Call function
        module.import_resource(
            table='table', schema='schema', data='data',
            backend='backend', **self.backend_options)

        # Assert calls
        self.import_module.assert_called_with('jsontableschema.plugins.backend')
        self.import_module.return_value.Storage.assert_called_with(**self.backend_options)
        self.ensure_dir.assert_has_calls([call('schema'), call('data')])
        self.open.assert_has_calls([
            call('schema', mode=ANY, encoding=ANY),
            call('data', 'wb')], any_order=True)
        self.storage.describe.assert_called_with('table')
        self.storage.read.assert_called_with('table')
