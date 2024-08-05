from django.core.validators import (RegexValidator)
from django.utils.translation import gettext_lazy as _

numeric_validator = RegexValidator(r'^\d+$', _('Only digit characters.'))