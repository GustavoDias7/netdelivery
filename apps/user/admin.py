from django.contrib import admin
from . import models
from . import forms
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from delivery.constants import (USER_WITHOUT_PERMISSIONS, USER_WITH_PERMISSIONS)

class EmployeerInline(admin.StackedInline):
    model = models.User
    extra = 0
    min_num = 0
    autocomplete_fields = ("owned_by",)
    exclude = ("password", "is_owner")
    fields = (
        "first_name", 
        "last_name", 
        "email", 
        "username", 
        "phone", 
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "user_permissions",
        "last_login",
        "date_joined"
    )
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        
        if obj and not request.user.is_superuser:
            return (
                "first_name", 
                "last_name", 
                "username", 
                "phone",
            )
        else:
            return fields
        
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        
        if obj and request.user.is_owner:
            return (
                "first_name", 
                "last_name", 
                "username", 
                "phone",
            )
        else:
            return readonly_fields

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    inlines = [EmployeerInline]
    list_display = ("email", "first_name", "last_name", "username", "is_staff")
    add_fieldsets = (
        (
            None, 
            { 
            'classes': ('wide',), 
            'fields': ('email', 'username', 'password1', 'password2')
            }
        ),
    )
    autocomplete_fields = ("owned_by",)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_owner:
            owner_and_employeers = Q(owned_by=request.user) | Q(username=request.user.username)
            return qs.filter(owner_and_employeers)
        else:
            return qs.filter(username=request.user.username)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        
        if obj and request.user.is_superuser:
            return USER_WITH_PERMISSIONS
        elif obj and not request.user.is_superuser:
            return USER_WITHOUT_PERMISSIONS
        else:
            return fieldsets

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "logradouro", "phone_", "cpf_")
    search_fields = ("full_name", "logradouro__cep", "logradouro__name", "phone", "cpf")
    autocomplete_fields = ("logradouro",)
    form = forms.ClientsForm
    
    @admin.display(description='phone')
    def phone_(self, obj):
        return obj.fphone()
    
    @admin.display(description='cpf')
    def cpf_(self, obj):
        return obj.fcpf()
    
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
    
    def get_changeform_initial_data(self, request):
        return {"user": request.user}
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(user=user)
    
    # def has_add_permission(self, request):
    #     return not self.model.objects.filter(user=request.user).exists()