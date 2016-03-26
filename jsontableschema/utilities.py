# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import sys
import json
import requests
from copy import deepcopy
from importlib import import_module

from . import compat
from . import exceptions


REMOTE_SCHEMES = ('http', 'https', 'ftp', 'ftps')
NULL_VALUES = ['null', 'none', 'nil', 'nan', '-', '']
TRUE_VALUES = ['yes', 'y', 'true', 't', '1', 1]
FALSE_VALUES = ['no', 'n', 'false', 'f', '0', 0]


def load_json_source(source):
    """Load a JSON source, from string, URL or buffer, into a Python type.
    """

    if source is None:
        return None

    elif isinstance(source, (dict, list)):
        # the source has already been loaded
        return deepcopy(source)

    if compat.parse.urlparse(source).scheme in REMOTE_SCHEMES:
        source = requests.get(source).text

    elif isinstance(source, compat.str) and not os.path.exists(source):
        pass

    else:
        with io.open(source, encoding='utf-8') as stream:
            source = stream.read()

    try:
        return json.loads(source)
    except ValueError as e:
        raise exceptions.InvalidJSONError


def ensure_dir(path):
    """Ensure directory exists.

    Parameters
    ----------
    path: str

    """
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)


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
