# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import json
import pytest
import requests
from tableschema.profile import Profile


# Tests

@pytest.mark.skipif(os.environ.get('TRAVIS_BRANCH') != 'master', reason='CI')
def test_specs_table_schema_is_up_to_date():
    profile = Profile('table-schema')
    jsonschema = requests.get('https://specs.frictionlessdata.io/schemas/table-schema.json').json()
    assert profile.jsonschema == jsonschema, 'run `make profiles` to update profiles'
