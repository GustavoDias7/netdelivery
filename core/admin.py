from django.contrib import admin
from . import models

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product_category", "id", "archived"]
    readonly_fields = ["id"]
    fields = [
        "id",
        "name",
        "price",
        "discount",
        "description",
        "stock",
        # "image",
        "archived",
        "product_category"
    ]
    

class ShippingTaxAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "id"]
    
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    
class OrderAdmin(admin.ModelAdmin):
    # list_display = []
    readonly_fields = []
    
    # def get_readonly_fields(self, request, obj=None):
    #     return list(self.readonly_fields) + \
    #         [field.name for field in obj._meta.fields] + \
    #         [field.name for field in obj._meta.many_to_many]
    
class OrderItempeAdmin(admin.ModelAdmin):
    # list_display = []
    readonly_fields = []
    
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ShippingTax, ShippingTaxAdmin)
admin.site.register(models.PaymentType, PaymentTypeAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItempeAdmin)
admin.site.register(models.OrderStatus)

