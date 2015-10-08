# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json

from jsonschema.validators import validator_for

from . import compat


def validate(schema):
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'json-table-schema.json')

    with open(filepath) as f:
        json_table_schema = json.load(f)

    valid = True
    Validator = validator_for(json_table_schema)
    validator = Validator(json_table_schema)
    errors = [e.message for e in validator.iter_errors(schema)]
    if errors:
        valid = False

    # the hash MAY contain a key `primaryKey`
    if isinstance(schema, dict) and schema.get('primaryKey'):
        # ensure that the primary key matches field names
        if isinstance(schema['primaryKey'], compat.str):
            if not schema['primaryKey'] in [f['name'] for f in schema['fields']]:
                valid = False
                errors.append('A JSON Table Schema primaryKey value must be '
                              'found in the schema field names')

        else:
            for k in schema['primaryKey']:
                if k not in [f['name'] for f in schema['fields']]:
                    valid = False
                    errors.append('A JSON Table Schema primaryKey value '
                                  'must be found in the schema field names')

    # the hash may contain a key `foreignKeys`
    if isinstance(schema, dict) and schema.get('foreignKeys'):
        for fk in schema['foreignKeys']:

            # ensure that `foreignKey.fields` match field names
            if isinstance(fk.get('fields'), compat.str):
                if fk.get('fields') not in [f['name'] for f in
                                            schema['fields']]:
                    valid = False
                    errors.append('A JSON Table Schema foreignKey.fields '
                                  'value must correspond with field names.')

            else:
                for field in fk.get('fields'):
                    if field not in [f['name'] for f in
                                     schema['fields']]:
                        valid = False
                        errors.append('A JSON Table Schema '
                                      'foreignKey.fields value must '
                                      'correspond with field names.')

            # ensure that `foreignKey.reference.fields`
            # matches outer `fields`
            if isinstance(fk.get('fields'), compat.str):
                if not isinstance(fk['reference']['fields'], compat.str):
                    valid = False
                    errors.append('A JSON Table Schema '
                                  'foreignKey.reference.fields must match '
                                  'field names.')
            else:
                if not len(fk.get('fields')) == len(fk['reference']['fields']):
                    valid = False
                    errors.append('A JSON Table Schema must have a fields '
                                  'key.')
    return valid, errors
