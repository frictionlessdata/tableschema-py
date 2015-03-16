# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import _types


def infer(headers, values, row_limit=None, strict=False, primary_key=None):

    """Return a schema from the passed headers and values.

    Args:
    * `headers`: a list of header names
    * `values`: a reader over data, yielding each row as a list of values
    * `strict`: require 100% compliance, or, be lenient in certain cases.
    * `primary_key`: pass in a primary key or iterable of keys.

    Returns:
    * A JSON Table Schema as a Python dict.

    """

    guesser = _types.TypeGuesser()
    resolver = _types.TypeResolver()
    schema = {'fields': []}
    type_matches = {}

    # TODO: Ensure that passed PKs are in headers
    if primary_key:
        schema['primaryKey'] = primary_key

    for header in headers:
        descriptor = {
            'name': header,
            'constraints': {
                'required': True,
            }
        }

        schema['fields'].append(descriptor)

    for index, row in enumerate(values):

        if row_limit and (index > row_limit):
            break

        else:

            # Normalize rows with invalid dimensions for sanity
            row_length = len(row)
            headers_length = len(headers)

            if row_length > headers_length:
                row = row[:len(headers)]

            if row_length < headers_length:
                diff = headers_length - row_length
                fill = [''] * diff
                row = row.extend(fill)

            # build a column-wise lookup of type matches
            for index, value in enumerate(row):
                rv = guesser.cast(value)

                if type_matches.get(index):
                    type_matches[index].append(rv)
                else:
                    type_matches[index] = [rv]

    # choose a type/format for each column based on the matches
    for index, results in type_matches.items():
        rv = resolver.get(results)
        schema['fields'][index].update(**rv)

    return schema
