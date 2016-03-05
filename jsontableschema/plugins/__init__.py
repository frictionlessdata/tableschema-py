# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ..utilities import PluginImporter


# Register importer
importer = PluginImporter(
    virtual='jsontableschema.plugins.',
    actual='jsontableschema_')
importer.register()

# Delete variables
del PluginImporter
del importer
