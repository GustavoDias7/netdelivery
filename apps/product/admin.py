from django.contrib import admin
from . import models
from . import forms
from django.utils.translation import gettext_lazy as _

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ("product__name", "size")
    readonly_fields = ("id",)
    
    def has_module_permission(self, request):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(product__user=user)
    
    
class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    min_num = 1
    form = forms.ProductVariantForm
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ("name", "category", "id",)
    list_filter = ("category__name",)
    readonly_fields = ("id",)
    form = forms.ProductForm
    
    def get_changeform_initial_data(self, request):
        return {"user": request.user}
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(user=user)


class ComboItemAdmin(admin.ModelAdmin):
    pass

class ComboItemInline(admin.StackedInline):
    model = models.ComboItem
    extra = 0
    min_num = 1
    autocomplete_fields = ("product_variant",)

@admin.register(models.Combo)
class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboItemInline]
    form = forms.ComboForm
    list_display = ("name", "price", "id", "archived")
    
    def get_changeform_initial_data(self, request):
        return {"user": request.user}
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(user=user)
