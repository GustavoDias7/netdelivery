from django.contrib import admin
from . import models
from . import forms
from django.contrib.auth.admin import UserAdmin
from apps.core.utils import remove_non_numeric

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

@admin.register(models.Contacts)
class ContactsAdmin(admin.ModelAdmin):
    form = forms.ContactsForm
    change_form_template = "admin/contacts_change_form.html"