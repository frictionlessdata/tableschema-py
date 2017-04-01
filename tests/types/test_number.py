# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
from decimal import Decimal
from tableschema import types
from tableschema.config import ERROR


# Tests

@pytest.mark.parametrize('format, value, options, result', [
    ('default', Decimal(1), {}, Decimal(1)),
    ('default', 1, {}, Decimal(1)),
    ('default', 1.0, {}, Decimal(1)),
    ('default', '1', {}, Decimal(1)),
    ('default', '10.00', {}, Decimal(10)),
    ('default', '10.50', {}, Decimal(10.5)),
    ('default', '100%', {}, Decimal(1)),
    ('default', '1000‰', {}, Decimal(10)),
    ('default', '-1000', {}, Decimal(-1000)),
    ('default', '1,000', {'groupChar': ','}, Decimal(1000)),
    ('default', '10,000.00', {'groupChar': ','}, Decimal(10000)),
    ('default', '10,000,000.50', {'groupChar': ','}, Decimal(10000000.5)),
    ('default', '10#000.00', {'groupChar': '#'}, Decimal(10000)),
    ('default', '10#000#000.50', {'groupChar': '#'}, Decimal(10000000.5)),
    ('default', '10.50', {'groupChar': '#'}, Decimal(10.5)),
    ('default', '1#000', {'groupChar': '#'}, Decimal(1000)),
    ('default', '10#000@00', {'groupChar': '#', 'decimalChar': '@'}, Decimal(10000)),
    ('default', '10#000#000@50', {'groupChar': '#', 'decimalChar': '@'}, Decimal(10000000.5)),
    ('default', '10@50', {'groupChar': '#', 'decimalChar': '@'}, Decimal(10.5)),
    ('default', '1#000', {'groupChar': '#', 'decimalChar': '@'}, Decimal(1000)),
    ('default', '10,000.00', {'groupChar': ',', 'currency': True}, Decimal(10000)),
    ('default', '10,000,000.00', {'groupChar': ',', 'currency': True}, Decimal(10000000)),
    ('default', '$10000.00', {'currency': True}, Decimal(10000)),
    ('default', '  10,000.00 €', {'groupChar': ',', 'currency': True}, Decimal(10000)),
    ('default', '10 000,00', {'groupChar': ' ', 'decimalChar': ','}, Decimal(10000)),
    ('default', '10 000 000,00', {'groupChar': ' ', 'decimalChar': ','}, Decimal(10000000)),
    ('default', '10000,00 ₪', {'groupChar': ' ', 'decimalChar': ',', 'currency': True}, Decimal(10000)),
    ('default', '  10 000,00 £', {'groupChar': ' ', 'decimalChar': ',', 'currency': True}, Decimal(10000)),
    ('default', '10,000a.00', {}, ERROR),
    ('default', '10+000.00', {}, ERROR),
    ('default', '$10:000.00', {}, ERROR),
    ('default', 'string', {}, ERROR),
    ('default', '', {}, ERROR),
])
def test_cast_number(format, value, options, result):
    assert types.cast_number(format, value, **options) == result
