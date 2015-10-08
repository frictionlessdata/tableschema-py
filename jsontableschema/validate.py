# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json

from jsonschema.validators import validator_for
from jsonschema.exceptions import ValidationError

from . import compat


def load_validator():
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'json-table-schema.json')
    with open(filepath) as f:
        json_table_schema = json.load(f)
    return json_table_schema, validator_for(json_table_schema)


json_table_schema, BaseValidator = load_validator()


class JSONTableSchemaValidator(BaseValidator):
    def iter_errors(self, instance, _schema=None):
        for error in super(JSONTableSchemaValidator, self).iter_errors(
                instance, _schema):
            yield error

        # the hash MAY contain a key `primaryKey`
        if isinstance(instance, dict) and instance.get('primaryKey'):
            # ensure that the primary key matches field names
            field_names = [f['name'] for f in instance['fields']]
            if isinstance(instance['primaryKey'], compat.str):
                if not instance['primaryKey'] in field_names:
                    yield ValidationError(
                        'A JSON Table Schema primaryKey value must be found in'
                        'the schema field names'
                    )
            else:
                for k in instance['primaryKey']:
                    if k not in field_names:
                        yield ValidationError(
                            'A JSON Table Schema primaryKey value must be '
                            'found in the schema field names'
                        )

        # the hash may contain a key `foreignKeys`
        if isinstance(instance, dict) and instance.get('foreignKeys'):
            for fk in instance['foreignKeys']:
                # ensure that `foreignKey.fields` match field names
                field_names = [f['name'] for f in instance['fields']]
                if isinstance(fk.get('fields'), compat.str):
                    if fk.get('fields') not in field_names:
                        yield ValidationError(
                            'A JSON Table Schema foreignKey.fields value must '
                            'correspond with field names.'
                        )
                else:
                    for field in fk.get('fields'):
                        if field not in field_names:
                            yield ValidationError(
                                'A JSON Table Schema foreignKey.fields value '
                                'must correspond with field names.'
                            )

                # ensure that `foreignKey.reference.fields`
                # matches outer `fields`
                if isinstance(fk.get('fields'), compat.str):
                    if not isinstance(fk['reference']['fields'], compat.str):
                        yield ValidationError(
                            'A JSON Table Schema foreignKey.reference.fields '
                            'must match field names.'
                        )
                else:
                    if not len(fk.get('fields')) == len(fk['reference']['fields']):
                        yield ValidationError(
                            'A JSON Table Schema must have a fields key.'
                        )


def validate(schema):
    valid = True
    validator = JSONTableSchemaValidator(json_table_schema)
    errors = [e.message for e in validator.iter_errors(schema)]
    if errors:
        valid = False
    return valid, errors
