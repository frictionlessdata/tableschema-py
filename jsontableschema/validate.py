# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json

import jsonschema
from jsonschema.validators import validator_for

from . import compat, exceptions


def load_validator():
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'schemas/json-table-schema.json')
    with open(filepath) as f:
        json_table_schema = json.load(f)
    return json_table_schema, validator_for(json_table_schema)


json_table_schema, BaseValidator = load_validator()


class JSONTableSchemaValidator(BaseValidator):
    @classmethod
    def check_schema(cls, schema):
        # When checking against the metaschema, we do not want to run the
        # additional checking added in iter_errors
        parent_cls = cls.__bases__[0]
        for error in parent_cls(cls.META_SCHEMA).iter_errors(schema):
            raise jsonschema.exceptions.SchemaError.create_from(error)

    def iter_errors(self, instance, _schema=None):
        for e in super(JSONTableSchemaValidator, self).iter_errors(instance,
                                                                   _schema):
            yield exceptions.SchemaValidationError(
                e.message, e.validator, e.path, e.cause, e.context,
                e.validator_value, e.instance, e.schema, e.schema_path,
                e.parent
            )

        try:
            field_names = [f['name'] for f in instance['fields']]
        except (TypeError, KeyError):
            field_names = []
        # the hash MAY contain a key `primaryKey`
        if isinstance(instance, dict) and instance.get('primaryKey'):
            # ensure that the primary key matches field names

            if isinstance(instance['primaryKey'], compat.str):
                if not instance['primaryKey'] in field_names:
                    yield exceptions.SchemaValidationError(
                        'A JSON Table Schema primaryKey value must be found in'
                        ' the schema field names'
                    )
            elif isinstance(instance['primaryKey'], list):
                for k in instance['primaryKey']:
                    if k not in field_names:
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema primaryKey value must be '
                            'found in the schema field names'
                        )

        # the hash may contain a key `foreignKeys`
        if isinstance(instance, dict) and instance.get('foreignKeys'):
            for fk in instance['foreignKeys']:
                # ensure that `foreignKey.fields` match field names
                if isinstance(fk.get('fields'), compat.str):
                    if fk.get('fields') not in field_names:
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields value must '
                            'correspond with field names.'
                        )
                elif isinstance(fk.get('fields', []), list):
                    for field in fk.get('fields'):
                        if field not in field_names:
                            yield exceptions.SchemaValidationError(
                                'A JSON Table Schema foreignKey.fields value '
                                'must correspond with field names.'
                            )

                # ensure that `foreignKey.reference.fields`
                # matches outer `fields`
                if isinstance(fk.get('fields'), compat.str):
                    if not isinstance(fk['reference']['fields'], compat.str):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.reference.fields '
                            'must match field names.'
                        )
                else:
                    if isinstance(fk['reference']['fields'], compat.str):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields cannot '
                            'be a string when foreignKey.reference.fields.'
                            'is a string'
                        )
                    if not len(fk.get('fields')) == len(fk['reference']['fields']):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields must '
                            'contain the same number entries as '
                            'foreignKey.reference.fields.'
                        )


validator = JSONTableSchemaValidator(json_table_schema)


def validate(schema):
    jsonschema.validate(schema, json_table_schema,
                        cls=JSONTableSchemaValidator)
    return True
