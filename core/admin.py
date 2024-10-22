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

@admin.register(models.PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    add_fieldsets = ((
        None, 
        { 'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}
    ))

admin.site.register(models.OrderItemStatus)

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    readonly_fields = (
        "price",
        "discount",
    )
    
@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "logradouro", "phone", "cpf")
    search_fields = ("full_name", "logradouro__cep", "logradouro__name", "phone", "cpf")
    autocomplete_fields = ("logradouro",)
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "client",
        "payment_type",
        "shipping_fee",
        "shipping_fee_value",
        "created",
        "received_date",
    )
    readonly_fields = (
        "payment_type_name",
        "payment_type_code",
        "shipping_fee_value",
        "created",
    )
    autocomplete_fields = ("client",)
    def save_model(self, request, obj, form, change):
        self.model.payment_type_name = "Test"
        super().save_model(request, obj, form, change)

@admin.register(models.ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "uf", "localidade", "value", "is_default")
    autocomplete_fields = ("whitelistbairro",)
    
    @admin.display(empty_value=_("Default"))
    def bairro_(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.name
    
    @admin.display(description='Localidade')
    def localidade(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.localidade.name
        else:
            return "-"
        
    @admin.display(description='uf')
    def uf(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.localidade.uf.acronym
        else:
            return "-"

@admin.register(models.OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "address_number",
        "address_complement",
        "uf_acronym",
        "logradouro_cep",
        "logradouro_name",
        "logradouro_type",
        "localidade_name",
        "bairro_name",
    )
    