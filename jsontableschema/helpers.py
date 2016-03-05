# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from importlib import import_module


class PluginImporter(object):
    """Plugin importer.
    Example
    -------
    Add to myapp.plugins something like that::
        importer = PluginImporter(virtual='myapp.plugins.', actual='myapp_')
        importer.register()
        del PluginImporter
        del importer
    """

    # Public

    def __init__(self, virtual, actual):
        self.__virtual = virtual
        self.__actual = actual

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.virtual == other.virtual and
                self.actual == other.actual)

    @property
    def virtual(self):
        return self.__virtual

    @property
    def actual(self):
        return self.__actual

    def register(self):
        if self not in sys.meta_path:
            sys.meta_path.append(self)

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.virtual):
            return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        if not fullname.startswith(self.virtual):
            raise ImportError(fullname)
        realname = fullname.replace(self.virtual, self.actual)
        try:
            module = import_module(realname)
        except ImportError:
            message = 'Plugin "%s" is not installed. '
            message += 'Run `pip install %s` to install.'
            message = message % (fullname, realname)
            raise ImportError(message)
        sys.modules[realname] = module
        sys.modules[fullname] = module
        return module
