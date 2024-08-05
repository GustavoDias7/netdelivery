from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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