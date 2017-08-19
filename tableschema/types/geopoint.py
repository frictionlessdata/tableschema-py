# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import json
from collections import namedtuple
from decimal import Decimal
from ..config import ERROR


# Module API

def cast_geopoint(format, value, **options):
    try:
        if format == 'default':
            if isinstance(value, six.string_types):
                lon, lat = value.split(',')
                lon = lon.strip()
                lat = lat.strip()
            elif isinstance(value, (tuple, list)):
                lon, lat = value
        elif format == 'array':
            if isinstance(value, six.string_types):
                value = json.loads(value)
            lon, lat = value
        elif format == 'object':
            if isinstance(value, six.string_types):
                value = json.loads(value)
            if len(value) != 2:
                return ERROR
            lon = value['lon']
            lat = value['lat']
        geopoint = _geopoint(Decimal(lon), Decimal(lat))
    except Exception:
        return ERROR
    if geopoint.lon > 180 or geopoint.lon < -180:
        return ERROR
    if geopoint.lat > 90 or geopoint.lat < -90:
        return ERROR
    return geopoint


# Internal

_geopoint = namedtuple('geopoint', ['lon', 'lat'])
_geopoint.__repr__ = lambda self: str([float(self[0]), float(self[1])])
