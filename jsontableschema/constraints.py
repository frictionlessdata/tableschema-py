from . import exceptions


class NoConstraintsSupportedMixin(object):

    '''All constraints raise a ConstraintNotSupported exception'''

    def check_minLength(self, value):
        '''Override in subclass if constraint is supported.'''
        raise exceptions.ConstraintNotSupported(
            msg="Field type '{0}' does not support the minLength constraint"
            .format(self.name))

    def check_maxLength(self, value):
        '''Override in subclass if constraint is supported.'''
        raise exceptions.ConstraintNotSupported(
            msg="Field type '{0}' does not support the maxLength constraint"
            .format(self.name))


class LengthConstraintMixin(object):

    def check_minLength(self, value, min_length):
        '''
        Check minLength constraint.

        Only applicable to sequences like string and array. Will raise
        TypeError if applied to other types. None applicable types should
        override and raise ConstraintNotSupported exception.
        '''
        if min_length is not None:
            if len(value) < min_length:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must have a minimum length of {1}"
                    .format(self.field_name, min_length))

    def check_maxLength(self, value, max_length):
        '''
        Check maxLength constraint.

        Only applicable to sequences like string and array. Will raise
        TypeError if applied to other types. None applicable types should
        override and raise ConstraintNotSupported exception.
        '''
        if max_length is not None:
            if len(value) > max_length:
                raise exceptions.ConstraintError(
                    msg="The field '{0}' must have a maximum length of {1}"
                    .format(self.field_name, max_length))
