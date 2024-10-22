from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ProductCategory)

class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    min_num = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

class ComboItemInline(admin.StackedInline):
    model = models.ComboItem
    extra = 0
    min_num = 1

@admin.register(models.Combo)
class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboItemInline]
