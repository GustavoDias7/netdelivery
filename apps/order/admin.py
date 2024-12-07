from django.contrib import admin
from . import models
from .forms import ShippingFeeForm
from django.utils.translation import gettext_lazy as _

@admin.register(models.PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

admin.site.register(models.OrderItemStatus)

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    readonly_fields = (
        "price",
        "discount",
    )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "client",
        "payment_type",
        "shipping_fee",
        "shipping_fee_value",
    )
    exclude = (
        "user",
        "payment_type_name",
        "payment_type_code",
        "shipping_fee_value",
        "created",
    )
    autocomplete_fields = ("client",)
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        self.model.payment_type_name = "Test"
        super().save_model(request, obj, form, change)
        
    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

@admin.register(models.ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "uf", "localidade", "value", "is_default")
    autocomplete_fields = ("bairro",)
    form = ShippingFeeForm
    
    def get_changeform_initial_data(self, request):
        return {"user": request.user}
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)
    
    @admin.display(description='Bairro')
    def bairro_(self, obj):
        if obj.bairro:
            return obj.bairro
        elif obj.is_default:
            return _("Default")
        else:
            return "-"
    
    @admin.display(description='Localidade')
    def localidade(self, obj):
        if obj.bairro:
            return obj.bairro.localidade.name
        else:
            return "-"
        
    @admin.display(description='uf')
    def uf(self, obj):
        if obj.bairro:
            return obj.bairro.localidade.uf.acronym
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

