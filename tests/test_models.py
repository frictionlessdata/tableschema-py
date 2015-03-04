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
                "constraints": {
                    "required": True,
                }
            },
            {
                "name": "height",
                "constraints": {
                    "required": False,
                }
            },
        ]
    }

    def test_headers(self):

        model = models.JSONTableSchema(self.schema)

        self.assertEqual(len(model.headers), 2)

    def test_required_headers(self):

        model = models.JSONTableSchema(self.schema)

        self.assertEqual(len(model.required_headers), 1)
