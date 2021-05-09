import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator:

    def __init__(self, reg_num='\d'):
        self.reg_num = reg_num

    def validate(self, password, user=None):
        if not re.findall(self.reg_num, password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator:

    def __init__(self, reg_upper='[A-Z]'):
        self.reg_upper = reg_upper

    def validate(self, password, user=None):
        if not re.findall(self.reg_upper, password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator:

    def __init__(self, reg_lowwer='[a-z]'):
        self.reg_lowwer = reg_lowwer

    def validate(self, password, user=None):
        if not re.findall(self.reg_lowwer, password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )
