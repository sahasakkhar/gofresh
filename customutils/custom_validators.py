from django.forms import EmailField
from customutils.full_scope_static import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH

__author__ = 'goutom roy'

from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class MinMaxLengthValidator(object):

    def __init__(self, min_length=6, max_length=30):

        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):

        if len(password) < self.min_length:

            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code='password_too_short',params={'min_length': self.min_length},)

        elif len(password) > self.max_length:

            raise ValidationError(
                _("This password must be at most %(max_length)d characters."),
                code='password_too_long',params={'max_length': self.max_length}, )

    def get_help_text(self):

        return _(
            "Your password must be between %(min_length)d to %(max_length) characters."
            % {'min_length': self.min_length, 'max_length': self.max_length}
        )


def is_email_address_valid(email):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False


def validate_password(password):

    import re
    match_result = re.match(r'^[0-9A-Za-z_-]*$', password)

    if len(password) < MIN_PASSWORD_LENGTH:
        msg = 'Password too short! Minimum 6 characters long.'
        return msg

    elif len(password) > MAX_PASSWORD_LENGTH:
        msg = 'Password too long! Maximum 30 characters long.'
        return msg

    elif match_result is None:
        msg = 'Only alphanumeric(a-zA-Z0-9) and' + "' - ', " + "'_'" + ' characters are allowed.'
        return msg
    msg = None
    return msg
