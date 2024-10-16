from django.contrib import admin
from . import models

# Register your models here.

# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ["name", "product_category", "id", "archived"]
#     readonly_fields = ["id"]
#     fields = [
#         "id",
#         "name",
#         "price",
#         "discount",
#         "description",
#         "stock",
#         # "image",
#         "archived",
#         "product_category"
#     ]

# admin.site.register(models.ProductCategory)

class PizzaVariantInline(admin.StackedInline):
    model = models.PizzaVariant
    extra = 0
    min_num = 1

@admin.register(models.Pizza)
class PizzaAdmin(admin.ModelAdmin):
    inlines = [PizzaVariantInline]

class SodaVariantInline(admin.StackedInline):
    model = models.SodaVariant
    extra = 0
    min_num = 1

@admin.register(models.Soda)
class SodaAdmin(admin.ModelAdmin):
    inlines = [SodaVariantInline]