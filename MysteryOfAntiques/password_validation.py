from __future__ import unicode_literals

import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class UpperLowerNumericPasswordValidator(object):
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if not re.search(r'\d', password) or \
            not re.search(r'[a-z]', password) or \
            not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contains Uppercase letters, Lowercase letters and numbers."),
                code='must-contains-uppercase-letters-lowercase-letters-and-numbers',
            )

    def get_help_text(self):
        return _("Your password must contains Uppercase letters, Lowercase letters and numbers.")
