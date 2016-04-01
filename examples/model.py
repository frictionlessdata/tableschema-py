# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from jsontableschema.model import SchemaModel


# Create schema model
schema = SchemaModel('data/schema_valid_simple.json')

# Convert a row
print(list(schema.convert_row('1', 'title1')))

# Convert a set of rows
print(list(schema.convert([['2', 'title2'], ['3', 'title3']])))
