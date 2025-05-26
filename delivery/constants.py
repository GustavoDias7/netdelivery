from django.utils.translation import gettext_lazy as _

DAY_OF_THE_WEEK = {
    '0': _('Monday'),
    '1': _('Tuesday'),
    '2': _('Wednesday'),
    '3': _('Thursday'),
    '4': _('Friday'),
    '5': _('Saturday'), 
    '6': _('Sunday'),
}

# PIZZA_SIZES = {
#     '1': _('Small'),
#     '2': _('Medium'),
#     '3': _('Large'),
#     '4': _('Giant'),
#     '5': _('Family'),
#     '6': _('Maracanã'),
# }

OPTION_TYPES = {
    '0': _('Single choice'),
    '1': _('Multiple choices'),
}

USER_OWNER = (
    (_("Personal info"), {"fields": ("first_name", "username", "phone")}),
)

USER_WITHOUT_PERMISSIONS = (
    (_("Personal info"), {"fields": ("first_name", "last_name", "username", "phone")}),
)

USER_WITH_PERMISSIONS = (
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
    (_("Permissions"), { "fields": ("is_active", "is_staff", "is_superuser", "is_owner", "owned_by", "groups", "user_permissions")}),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)