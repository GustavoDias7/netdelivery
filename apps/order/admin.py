from django.contrib import admin
from . import models
from apps.product.models import ProductVariant, Combo
from .forms import ShippingFeeForm, OrderForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models.functions import Now
from django.utils.html import format_html

import locale 

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

@admin.register(models.PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

@admin.register(models.OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    exclude = []

    def get_readonly_fields(self, request, obj=None):
        if obj == None: return ()
        else:
            return (
                "product",
                "combo",
                "product_name",
                "price",
                "discount",
                "quantity",
            )
            
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj)
        if obj == None: 
            exclude.append("product_name")
            exclude.append("price")
            exclude.append("discount")
            return exclude
        else:
            return exclude
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = ProductVariant.objects.filter(product__user=request.user, archived=False)
        if db_field.name == "combo":
            kwargs["queryset"] = Combo.objects.filter(user=request.user, archived=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "created_",
        "order_status_",
        "payment_type",
        "shipping_fee_value_",
    )
    list_filter = ("order_status", "created")
    exclude = ["user_owner"]
    autocomplete_fields = ("client",)
    change_form_template = 'admin/order_change_form.html'
    form = OrderForm
    
    @admin.display(description=_("Shipping fee value"))
    def shipping_fee_value_(self, obj):
        if obj.shipping_fee_value:
            return locale.currency(obj.shipping_fee_value / 100, grouping=True)
        else:
            return None
    
    @admin.display(description=_("Created"))
    def created_(self, obj):
        return obj.created.strftime("%d/%m/%Y %H:%M:%S")
    
    def order_status_(self, obj):
        return format_html(
            '<span class="status {0}">{1}</span>',
            obj.order_status.code,
            obj.order_status.name
        )

    def get_readonly_fields(self, request, obj=None):
        readonly = []
        
        if obj == None:
            return readonly
        else:
            readonly.append("user_request")
            readonly.append("client")
            readonly.append("order_status")
            readonly.append("payment_type")
            readonly.append("payment_type_name")
            readonly.append("change_to") 
            readonly.append("shipping_fee")
            readonly.append("shipping_fee_value")
            readonly.append("created")
            readonly.append("received_date")
            return readonly
            
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj)
        if obj == None: 
            exclude.append("user_request")
            exclude.append("order_status")
            exclude.append("payment_type_name")
            exclude.append("shipping_fee_value")
            exclude.append("created")
            exclude.append("received_date")
            return exclude
        else:
            return exclude
        
    def has_delete_permission(self, request, obj=None):
        return False
        
    def get_changeform_initial_data(self, request):
        user = request.user.owner if request.user.owner else request.user
        return {"user_owner": user}
    
    def save_model(self, request, obj, form, change):
        obj.user_owner = request.user.owner if request.user.owner else request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owner if request.user.owner else request.user
        return qs.filter(user_owner=user)
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        
        try:
            extra_context["status"] = models.OrderStatus.objects.all().exclude(code="wating")
            extra_context["current_status"] = self.model.objects.get(id=object_id).order_status.code
        except ObjectDoesNotExist:
            extra_context["status"] = None
        
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )
        
    def response_change(self, request, obj):
        if "status" in request.POST:
            status = request.POST.get("status")
            try:
                order_status = models.OrderStatus.objects.get(code=status)
                obj.order_status = order_status
                if status == "delivered":
                    obj.received_date = Now()
                obj.save()
            except ObjectDoesNotExist:
                pass
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shipping_fee":
            kwargs["queryset"] = models.ShippingFee.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(models.ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "uf", "localidade", "value_", "is_default")
    autocomplete_fields = ("bairro",)
    form = ShippingFeeForm
    
    def get_changeform_initial_data(self, request):
        return {"user": request.user}
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owner if request.user.owner else request.user
        return qs.filter(user=user)
    
    @admin.display(description=_("Value"))
    def value_(self, obj):
        if obj.value:
            return locale.currency(obj.value / 100, grouping=True)
        else:
            return None
    
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
        elif obj.is_default:
            return _("Default")
        else:
            return "-"
        
    @admin.display(description='uf')
    def uf(self, obj):
        if obj.bairro:
            return obj.bairro.localidade.uf.acronym
        elif obj.is_default:
            return _("Default")
        else:
            return "-"

