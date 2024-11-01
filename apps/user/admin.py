from django.contrib import admin
from . import models
from . import forms
from django.contrib.auth.admin import UserAdmin

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
    form = forms.ClientsForm
    
# @admin.register(models.OpeningHours)
class OpeningHoursAdmin(admin.StackedInline):
    form = forms.OpeningHoursForm
    model = models.OpeningHours
    extra = 0
    min_num = 1

@admin.register(models.Contacts)
class ContactsAdmin(admin.ModelAdmin):
    inlines = [OpeningHoursAdmin]
    form = forms.ContactsForm
    
    def has_add_permission(self, request):
        return not models.Contacts.objects.exists()