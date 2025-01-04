from django.contrib import admin
from . import models
from . import forms
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class EmployeerInline(admin.StackedInline):
    model = models.User
    extra = 0
    min_num = 0
    autocomplete_fields = ("owned_by",)
    exclude = ("password", "is_owner")
    fields = (
        "username", 
        "first_name", 
        "last_name", 
        "email", 
        "phone", 
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "user_permissions",
        "last_login",
        "date_joined"
    )

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
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_owner",
                    "owned_by",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
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