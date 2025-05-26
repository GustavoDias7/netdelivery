from django.contrib import admin
import nested_admin
from . import models
from . import forms
from django.utils.translation import gettext_lazy as _

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

class OptionInline(nested_admin.NestedTabularInline):
    model = models.Option
    extra = 0
    min_num = 1
    max_num = 5
    template = 'admin/option_tabular_inline.html'
    form = forms.OptionForm

@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    pass

class OptionGroupInline(nested_admin.NestedTabularInline):
    model = models.OptionGroup
    extra = 0
    min_num = 0
    max_num = 1
    can_delete = True
    inlines = [OptionInline]
    template = 'admin/option_group_tabular_inline.html'
    

@admin.register(models.OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    pass

class ProductVariantInline(nested_admin.NestedStackedInline):
    model = models.ProductVariant
    extra = 0
    min_num = 1
    form = forms.ProductVariantForm
    inlines = [OptionGroupInline]
    
@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ("product__name", "name")
    readonly_fields = ("id",)
    inlines = [OptionGroupInline]
    
    def has_module_permission(self, request):
        return True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(product__user=user)

@admin.register(models.Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
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
