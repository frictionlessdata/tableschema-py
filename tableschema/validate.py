# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import jsonschema
from jsonschema.validators import validator_for
from . import exceptions
from . import specs


# Module API


def validate(descriptor, no_fail_fast=False):
    """Validate Table Schema schema descriptor.

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
            descriptor, specs.table_schema, cls=_TableSchemaValidator)

    # Multiple errors
    else:
        validator = _TableSchemaValidator(specs.table_schema)
        errors = list(validator.iter_errors(descriptor))
        if errors:
            raise exceptions.MultipleInvalid(errors=errors)

    return True


# Internal


class _TableSchemaValidator(validator_for(specs.table_schema)):
    @classmethod
    def check_schema(cls, schema):
        # When checking against the metaschema, we do not want to run the
        # additional checking added in iter_errors
        parent_cls = cls.__bases__[0]
        for error in parent_cls(cls.META_SCHEMA).iter_errors(schema):
            raise jsonschema.exceptions.SchemaError.create_from(error)

    def iter_errors(self, instance, _schema=None):

        for e in super(_TableSchemaValidator, self).iter_errors(
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
            if isinstance(instance['primaryKey'], list):
                for k in instance['primaryKey']:
                    if k not in field_names:
                        yield exceptions.SchemaValidationError(
                            'A Table Schema primaryKey value must be '
                            'found in the schema field names')

        # the hash may contain a key `foreignKeys`
        if isinstance(instance, dict) and instance.get('foreignKeys'):
            for fk in instance['foreignKeys']:

                # ensure that `foreignKey.fields` match field names
                if isinstance(fk.get('fields', []), list):
                    for field in fk.get('fields'):
                        if field not in field_names:
                            yield exceptions.SchemaValidationError(
                                'A Table Schema foreignKey.fields value '
                                'must correspond with field names.')
                    if not (len(fk.get('fields')) ==
                            len(fk['reference']['fields'])):
                        yield exceptions.SchemaValidationError(
                            'A Table Schema foreignKey.fields must '
                            'contain the same number entries as '
                            'foreignKey.reference.fields.')
