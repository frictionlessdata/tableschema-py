# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

from .schema import Schema
from .field import Field
from .table import Table
from .storage import Storage
from .validate import validate
from .infer import infer
from . import exceptions


# Version

import io
import os
__version__ = io.open(
    os.path.join(os.path.dirname(__file__), 'VERSION'),
    encoding='utf-8').read().strip()
