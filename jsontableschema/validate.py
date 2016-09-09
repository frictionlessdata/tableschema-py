# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import warnings
import jsonschema
from jsonschema.validators import validator_for
from . import compat, exceptions


# Module API

def validate(descriptor, no_fail_fast=False):
    """Validate JSON Table Schema schema descriptor.

    Args:
        descriptor (dict): schema descriptor to validate
        no_fail_fast (bool): collect all errors

    Raises:
        exceptions.SchemaValidationError
        exceptions.MultipleInvalid (no_fail_fast=True)

    Returns:
        bool: True

    """

    # Fail fast
    if not no_fail_fast:
        jsonschema.validate(
            descriptor, _json_table_schema,
            cls=_JSONTableSchemaValidator)

    # Multiple errors
    else:
        validator = _JSONTableSchemaValidator(_json_table_schema)
        errors = list(validator.iter_errors(descriptor))
        if errors:
            raise exceptions.MultipleInvalid(errors=errors)

    return True


# Deprecated
class Validator(object):
    @staticmethod
    def iter_errors(schema):
        # DEPRECATED [v0.7-v1)
        message = 'validator is deprecated [v0.7-v1)'
        warnings.warn(message, UserWarning)
        validator = _JSONTableSchemaValidator(_json_table_schema)
        return validator.iter_errors(schema)
validator = Validator()


# Internal

# Get schema and validator
def _load_schema_and_validator():
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'schemas/json-table-schema.json')
    with open(filepath) as file:
        json_table_schema = json.load(file)
    BaseValidator = validator_for(json_table_schema)
    return json_table_schema, BaseValidator
_json_table_schema, _BaseValidator = _load_schema_and_validator()


class _JSONTableSchemaValidator(_BaseValidator):
    @classmethod
    def check_schema(cls, schema):
        # When checking against the metaschema, we do not want to run the
        # additional checking added in iter_errors
        parent_cls = cls.__bases__[0]
        for error in parent_cls(cls.META_SCHEMA).iter_errors(schema):
            raise jsonschema.exceptions.SchemaError.create_from(error)

    def iter_errors(self, instance, _schema=None):

        for e in super(_JSONTableSchemaValidator, self).iter_errors(
                instance, _schema):
            yield exceptions.SchemaValidationError(
                e.message, e.validator, e.path, e.cause, e.context,
                e.validator_value, e.instance, e.schema, e.schema_path,
                e.parent)

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
                        ' the schema field names')
            elif isinstance(instance['primaryKey'], list):
                for k in instance['primaryKey']:
                    if k not in field_names:
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema primaryKey value must be '
                            'found in the schema field names')

        # the hash may contain a key `foreignKeys`
        if isinstance(instance, dict) and instance.get('foreignKeys'):
            for fk in instance['foreignKeys']:
                # ensure that `foreignKey.fields` match field names
                if isinstance(fk.get('fields'), compat.str):
                    if fk.get('fields') not in field_names:
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields value must '
                            'correspond with field names.')
                elif isinstance(fk.get('fields', []), list):
                    for field in fk.get('fields'):
                        if field not in field_names:
                            yield exceptions.SchemaValidationError(
                                'A JSON Table Schema foreignKey.fields value '
                                'must correspond with field names.')

                # ensure that `foreignKey.reference.fields`
                # matches outer `fields`
                if isinstance(fk.get('fields'), compat.str):
                    if not isinstance(fk['reference']['fields'], compat.str):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.reference.fields '
                            'must match field names.')
                else:
                    if isinstance(fk['reference']['fields'], compat.str):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields cannot '
                            'be a string when foreignKey.reference.fields.'
                            'is a string')
                    if not (len(fk.get('fields')) ==
                            len(fk['reference']['fields'])):
                        yield exceptions.SchemaValidationError(
                            'A JSON Table Schema foreignKey.fields must '
                            'contain the same number entries as '
                            'foreignKey.reference.fields.')
