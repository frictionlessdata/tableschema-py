# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from tableschema.exceptions import CastError


# Tests

def test_no_errors_reuse():
    ce1 = CastError('message1')
    ce1.errors.append('error')
    ce2 = CastError('message2')
    assert len(ce2.errors) == 0
