from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _

# Register your models here.

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
        "created",
        "received_date",
    )
    exclude = (
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
    list_display = ("bairro", "uf", "localidade", "value", "is_default")
    autocomplete_fields = ("bairro",)
    
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

