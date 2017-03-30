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

def cast_geopoint_default(value):
    geopoint = _extract_geopoint(value)
    if not geopoint:
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            lon, lat = value.split(',')
            geopoint = {'lon': Decimal(lon.strip()), 'lat': Decimal(lat.strip())}
        except Exception:
            return ERROR
    if not _validate_geopoint(geopoint):
        return ERROR
    return geopoint


def cast_geopoint_array(value):
    geopoint = _extract_geopoint(value)
    if not geopoint:
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            lon, lat = json.loads(value)
            geopoint = {'lon': Decimal(lon), 'lat': Decimal(lat)}
        except Exception:
            return ERROR
    if not _validate_geopoint(geopoint):
        return ERROR
    return geopoint


def cast_geopoint_object(value):
    geopoint = _extract_geopoint(value)
    if not geopoint:
        if not isinstance(value, six.string_types):
            return ERROR
        try:
            value = json.loads(value)
            if len(value) != 2:
                return ERROR
            geopoint = {'lon': Decimal(value['lon']), 'lat': Decimal(value['lat'])}
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
