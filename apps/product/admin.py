from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(models.Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass
    
class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    min_num = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ("name", "category",)
    list_filter = ("category__name",)
    change_form_template = "admin/product_change_form.html"

class ComboItemInline(admin.StackedInline):
    model = models.ComboItem
    extra = 0
    min_num = 1

@admin.register(models.Combo)
class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboItemInline]
