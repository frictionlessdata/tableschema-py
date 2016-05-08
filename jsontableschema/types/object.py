# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
from future.utils import raise_with_traceback
from .. import exceptions
from .. import utilities
from . import base


# Module API

class ObjectType(base.JTSType):

    # Public

    name = 'object'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
        'minLength',
        'maxLength',
    ]
    # ---
    python_type = dict

    def cast_default(self, value, fmt=None):

        if isinstance(value, self.python_type):
            return value

        try:
            json_value = json.loads(value)
            if isinstance(json_value, self.python_type):
                return json_value
            else:
                raise exceptions.InvalidObjectType()
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidObjectType(e))
