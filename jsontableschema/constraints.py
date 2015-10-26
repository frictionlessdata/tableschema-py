from dateutil.parser import parse as date_parse

from . import exceptions


class NoConstraintsSupportedMixin(object):

    '''All constraints raise a ConstraintNotSupported exception'''

    def _raise_constraint_not_supported(self, field_type, constraint):
        raise exceptions.ConstraintNotSupported(
            msg="Field type '{0}' does not support the {1} constraint"
            .format(field_type, constraint))

    def check_minLength(self, value):
        self._raise_constraint_not_supported(self.name, 'minLength')

    def check_maxLength(self, value):
        self._raise_constraint_not_supported(self.name, 'maxLength')

    def check_minimum(self, value):
        self._raise_constraint_not_supported(self.name, 'minimum')

    def check_maximum(self, value):
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
            if self.name in ('date', 'datetime'):
                minimum = date_parse(minimum, ignoretz=True)
            if self.name == 'date':
                minimum = minimum.date()
            if value < minimum:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must not be less than {1}"
                    .format(self.field_name, minimum))

    def check_maximum(self, value, maximum):
        if maximum is not None:
            if self.name in ('date', 'datetime'):
                maximum = date_parse(maximum, ignoretz=True)
            if self.name == 'date':
                maximum = maximum.date()
            if value > maximum:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must not be more than {1}"
                    .format(self.field_name, maximum))
