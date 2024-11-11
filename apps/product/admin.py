from django.contrib import admin
from . import models
from . import forms
from django.utils.translation import gettext_lazy as _
import os
from pprint import pprint

@admin.register(models.Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass
    
class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    min_num = 1
    form = forms.ProductVariantForm

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ("name", "category",)
    list_filter = ("category__name",)

class ComboItemInline(admin.StackedInline):
    model = models.ComboItem
    extra = 0
    min_num = 1

@admin.register(models.Combo)
class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboItemInline]
    form = forms.ComboForm
