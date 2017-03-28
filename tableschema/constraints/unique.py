# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


# Module API

def check_unique(name, values):
    """Unique values constraint.

    Raises:
        ConstraintNotSupported: always

    """
    raise exceptions.ConstraintNotSupported(
        'Unique constraint is not supported')
