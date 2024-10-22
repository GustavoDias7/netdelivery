from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

class CustomAutocompleteJsonView(AutocompleteJsonView):
    def serialize_result(self, obj, to_field_name):
        text = str(obj.select2() if obj.select2 else obj)
        return {'id': str(getattr(obj, to_field_name)), 'text': text}  

def autocomplete_view(self, request):
    return CustomAutocompleteJsonView.as_view(admin_site=self)(request)

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    add_fieldsets = ((
        None, 
        { 'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}
    ))


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "logradouro", "phone", "cpf")
    search_fields = ("full_name", "logradouro__cep", "logradouro__name", "phone", "cpf")
    autocomplete_fields = ("logradouro",)
