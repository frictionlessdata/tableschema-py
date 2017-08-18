# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .profile import Profile
from . import helpers


# Module API


def validate(descriptor):
    """https://github.com/frictionlessdata/tableschema-py#schema
    """

    # Process descriptor
    descriptor = helpers.retrieve_descriptor(descriptor)
    descriptor = helpers.expand_schema_descriptor(descriptor)

    # Get descriptor profile
    profile = Profile('table-schema')

    # Validate descriptor
    return profile.validate(descriptor)
