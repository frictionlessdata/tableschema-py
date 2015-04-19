# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import requests
from . import compat
from . import exceptions


REMOTE_SCHEMES = ('http', 'https', 'ftp', 'ftps')

NULL_VALUES = ['null', 'none', 'nil', 'nan', '-', '']

TRUE_VALUES = ['yes', 'y', 'true', 't', '1']

FALSE_VALUES = ['no', 'n', 'false', 'f', '0']


def load_json_source(source):

    """Load a JSON source, from string, URL or buffer,  into a Python type."""

    if source is None:
        return None

    elif isinstance(source, (dict, list)):
        # the source has already been loaded
        return source

    if compat.parse.urlparse(source).scheme in REMOTE_SCHEMES:
        source = requests.get(source).text

    elif isinstance(source, compat.str) and not os.path.exists(source):
        pass

    else:
        with io.open(source, encoding='utf-8') as stream:
            source = stream.read()

    try:
        return json.loads(source)
    except ValueError as e:
        raise exceptions.InvalidJSONError
