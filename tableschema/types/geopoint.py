# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import json
from decimal import Decimal
from ..config import ERROR


# Module API

def cast_geopoint(format, value):
    geopoint = _extract_geopoint(value)
    if not geopoint:
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            if format == 'default':
                lon, lat = value.split(',')
                geopoint = {
                    'lon': Decimal(lon.strip()),
                    'lat': Decimal(lat.strip()),
                }
            elif format == 'array':
                lon, lat = json.loads(value)
                geopoint = {
                    'lon': Decimal(lon),
                    'lat': Decimal(lat),
                }
            elif format == 'object':
                value = json.loads(value)
                if len(value) != 2:
                    return ERROR
                geopoint = {
                    'lon': Decimal(value['lon']),
                    'lat': Decimal(value['lat']),
                }
        except Exception:
            return ERROR
    if not _validate_geopoint(geopoint):
        return ERROR
    return geopoint


# Internal

def _extract_geopoint(value):
    if not isinstance(value, dict):
        return None
    if len(value) != 2:
        return None
    return {'lon': value['lon'], 'lat': value['lat']}


def _validate_geopoint(geopoint):
    if geopoint['lon'] > 180 or geopoint['lon'] < -180:
        return False
    elif geopoint['lat'] > 90 or geopoint['lat'] < -90:
        return False
    return True
