from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

numeric_validator = RegexValidator(r'^\d+$', _('Only digit characters.'))
    
def name_validator(value: str):
    if not value.isalpha():
        raise ValidationError(
            _("Must contain only letters."),
            params={"value": value},
        )
    elif len(value) < 3:
        raise ValidationError(
            _("Minimum 3 letters"),
            params={"value": value},
        )
        
def phone_validator(value: str):
    if not value.isnumeric():
        raise ValidationError(
            _("Only digit characters"),
            params={"value": value},
        )
    elif len(value) != 11:
        raise ValidationError(
            _("Must have 11 digits"),
            params={"value": value},
        )
    elif value[2] != "9":
        raise ValidationError(
            _("The third digit must be 9"),
            params={"value": value},
        )
        