# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import decimal
from future.utils import raise_with_traceback
from .. import exceptions
from .. import utilities
from .. import compat
from . import base


# Module API

class GeoPointType(base.JTSType):

    # Public

    name = 'geopoint'
    null_values = utilities.NULL_VALUES
    supported_constraints = [
        'required',
        'pattern',
        'enum',
    ]
    # ---
    python_types = (compat.str, list, dict)

    def cast_default(self, value, fmt=None):
        try:
            if isinstance(value, self.python_types):
                points = value.split(',')
                if len(points) == 2:
                    try:
                        geopoints = [decimal.Decimal(points[0].strip()),
                                     decimal.Decimal(points[1].strip())]
                        self.__check_latitude_longtiude_range(geopoints)
                        return geopoints
                    except decimal.DecimalException as e:
                        raise_with_traceback(exceptions.InvalidGeoPointType(e))
                else:
                    raise exceptions.InvalidGeoPointType(
                        '{0}: point is not of length 2'.format(value))
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidGeoPointType(e))

    def cast_array(self, value, fmt=None):
        try:
            json_value = json.loads(value)
            if isinstance(json_value, list) and len(json_value) == 2:
                try:
                    longitude = json_value[0].strip()
                    latitude = json_value[1].strip()
                except AttributeError:
                    longitude = json_value[0]
                    latitude = json_value[1]

                try:
                    geopoints = [decimal.Decimal(longitude),
                                 decimal.Decimal(latitude)]
                    self.__check_latitude_longtiude_range(geopoints)
                    return geopoints
                except decimal.DecimalException as e:
                    raise_with_traceback(exceptions.InvalidGeoPointType(e))
            else:
                raise exceptions.InvalidGeoPointType(
                    '{0}: point is not of length 2'.format(value))
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidGeoPointType(e))

    def cast_object(self, value, fmt=None):
        try:
            json_value = json.loads(value)

            try:
                longitude = json_value['longitude'].strip()
                latitude = json_value['latitude'].strip()
            except AttributeError:
                longitude = json_value['longitude']
                latitude = json_value['latitude']
            except KeyError as e:
                raise_with_traceback(exceptions.InvalidGeoPointType(e))

            try:
                geopoints = [decimal.Decimal(longitude),
                             decimal.Decimal(latitude)]
                self.__check_latitude_longtiude_range(geopoints)
                return geopoints
            except decimal.DecimalException as e:
                raise_with_traceback(exceptions.InvalidGeoPointType(e))
        except (TypeError, ValueError) as e:
            raise_with_traceback(exceptions.InvalidGeoPointType(e))

    # Private

    def __check_latitude_longtiude_range(self, geopoint):
        longitude = geopoint[0]
        latitude = geopoint[1]
        if longitude >= 180 or longitude <= -180:
            raise exceptions.InvalidGeoPointType(
                'longtitude should be between -180 and 180, '
                'found: {0}'.format(longitude)
            )
        elif latitude >= 90 or latitude <= -90:
            raise exceptions.InvalidGeoPointType(
                'latitude should be between -90 and 90, '
                'found: {0}'.format(latitude))
