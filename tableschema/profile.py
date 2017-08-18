# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import json
import jsonschema
from jsonschema.validators import validator_for
from . import exceptions


# Module API

class Profile(object):

    # Public

    def __init__(self, profile):
        self.__profile = profile
        self.__jsonschema = _PROFILES.get(profile)
        if not self.__jsonschema:
            message= 'Can\'t load profile "%s"' % profile
            raise exceptions.LoadError(message)

    @property
    def name(self):
        return self.__jsonschema.get('title', '').replace(' ', '-').lower() or None

    @property
    def jsonschema(self):
        return self.__jsonschema

    def validate(self, descriptor):
        if self.name != 'table-schema':
            return jsonschema.validate(descriptor, self.jsonschema)
        validator = _TableSchemaValidator(self.jsonschema)
        errors = list(validator.iter_errors(descriptor))
        if errors:
            message = 'There are %s validation errors (see exception.errors)' % len(errors)
            raise exceptions.ValidationError(message, errors=errors)
        return True


# Internal

def _load_profile(filename):
    path = os.path.join(os.path.dirname(__file__), 'profiles', filename)
    profile = json.load(io.open(path, encoding='utf-8'))
    return profile


_PROFILES = {
    'table-schema': _load_profile('table-schema.json'),
    'geojson': _load_profile('geojson.json'),
}


class _TableSchemaValidator(validator_for(_PROFILES['table-schema'])):
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
            yield jsonschema.exceptions.ValidationError(
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
