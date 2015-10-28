import re

from dateutil.parser import parse as date_parse

from . import compat
from . import exceptions


class ConstraintsNotSupportedMixin(object):

    '''Unsupported constraints raise a ConstraintNotSupported exception. Use
    for types that don't naturally support a constraint.'''

    def _raise_constraint_not_supported(self, field_type, constraint):
        raise exceptions.ConstraintNotSupported(
            msg="Field type '{0}' does not support the {1} constraint"
            .format(field_type, constraint))

    def check_minLength(self, value, min_length):
        self._raise_constraint_not_supported(self.name, 'minLength')

    def check_maxLength(self, value, max_length):
        self._raise_constraint_not_supported(self.name, 'maxLength')

    def check_minimum(self, value, minimum):
        self._raise_constraint_not_supported(self.name, 'minimum')

    def check_maximum(self, value, maximum):
        self._raise_constraint_not_supported(self.name, 'maximum')


class LengthConstraintMixin(object):

    '''
    Only applicable to sequences like string and array. Will raise TypeError
    if applied to other types. None applicable types should override and raise
    ConstraintNotSupported exception.
    '''

    def check_minLength(self, value, min_length):
        if min_length is not None and len(value) < min_length:
            raise exceptions.ConstraintError(
                msg="The field '{0}' must have a minimum length of {1}"
                .format(self.field_name, min_length))

    def check_maxLength(self, value, max_length):
        if max_length is not None and len(value) > max_length:
            raise exceptions.ConstraintError(
                msg="The field '{0}' must have a maximum length of {1}"
                .format(self.field_name, max_length))


class MinMaxConstraintMixin(object):

    '''
    Only applicable to numbers and date/times. Will raise TypeError if applied
    to other types. None applicable types should override and raise
    ConstraintNotSupported exception.
    '''

    def check_minimum(self, value, minimum):
        if minimum is not None:
            if self.name in ('date', 'datetime', 'time'):
                minimum = date_parse(minimum, ignoretz=True)
            if self.name == 'date':
                minimum = minimum.date()
            if self.name == 'time':
                minimum = minimum.time()
            if value < minimum:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must not be less than {1}"
                    .format(self.field_name, minimum))

    def check_maximum(self, value, maximum):
        if maximum is not None:
            if self.name in ('date', 'datetime', 'time'):
                maximum = date_parse(maximum, ignoretz=True)
            if self.name == 'date':
                maximum = maximum.date()
            if self.name == 'time':
                maximum = maximum.time()
            if value > maximum:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must not be more than {1}"
                    .format(self.field_name, maximum))


class EnumConstraintMixin(object):

    def _cast_enum(self, enum):
        '''
        Cast each member of the enum array as the same type and format of
        self. This ensures we're comparing like for like. Don't apply the
        type's constraints for this cast.
        '''
        return [self.cast(m, skip_constraints=True) for m in enum]

    def check_enum(self, value, enum):
        if value not in self._cast_enum(enum):
            raise exceptions.ConstraintError(
                msg="The value for field '{0}' must be in the enum array"
                .format(self.field_name))


class PatternConstraintMixin(object):

    '''Pattern constraint should be checked as a string value before the value
    is cast'''

    def check_pattern(self, value, pattern):
        '''`value` is treated as a string and must match the XML Schema Reg
        Exp `pattern`.'''

        # convert to str if necessary
        if not isinstance(value, compat.str):
            value = compat.str(value)

        p = re.compile('^{0}$'.format(pattern))
        p_match = p.match(value)
        if not p_match:
            raise exceptions.ConstraintError(
                msg="The value for field '{0}' must match the pattern"
                .format(self.field_name))
