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
    
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
