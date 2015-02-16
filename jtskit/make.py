# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def make(headers, values):

    """Return a schema from the passed headers and values.

    Args:
    * `headers`: a list of header names
    * `values`: an iterable of data (possible a sample of a whole dataset)

    Returns:
    * A JSON Table Schema as a Python dict.

    """

    # TODO: This is just a sketch out of the idea. Finish it.

    schema = {'fields': []}

    for header in headers:
        schema['fields'].append({'name': header})

    for row in values:
        assert len(row) == len(headers)

    # DO type guessing etc. See messy tables (or drop it straight in here).

    return schema
