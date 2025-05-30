from django.contrib import admin
from . import models
from apps.product.models import ProductVariant, Combo
from apps.order.forms import ShippingFeeForm, OrderForm, OrderItemInlineForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models.functions import Now
from django.utils.html import format_html
import locale 


@admin.register(models.PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    form = OrderItemInlineForm
    extra = 0
    min_num = 1
    exclude = []
    
    @admin.display(description=_("price"))
    def fprice(self, obj: models.OrderItem=None):
        return obj.fprice()
    
    @admin.display(description=_("discount"))
    def fdiscount(self, obj: models.OrderItem=None):
        return obj.fpercentage_discount()
    
    @admin.display(description=_("total"))
    def ftotal(self, obj: models.OrderItem=None):
        return obj.ftotal()
    
    def get_readonly_fields(self, request, obj=None):
        readonly = []
        
        if obj == None:
            return readonly
        else:
            readonly.append("product_name")
            readonly.append("fprice")
            readonly.append("fdiscount")
            readonly.append("quantity")
            readonly.append("ftotal")
                    
            return readonly
    
    def get_exclude(self, request, obj=None):
        exclude = []
        
        if obj == None: 
            exclude.append("product_name")
            exclude.append("price")
            exclude.append("discount")
            
            return exclude
        else:
            exclude.append("product")
            exclude.append("price")
            exclude.append("combo")
            exclude.append("discount")
            exclude.append("total")
            
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
        "fstatus",
        "payment_type",
        "fshipping_fee_value",
    )
    list_filter = ("status", "created")
    autocomplete_fields = ("client",)
    change_form_template = 'admin/order_change_form.html'
    
    @admin.display(description=_("shipping fee"))
    def fshipping_fee_value(self, obj: models.Order):
        if obj.shipping_fee_value:
            return locale.currency(obj.shipping_fee_value / 100, grouping=True)
        else:
            return None
    
    @admin.display(description=_("change to"))
    def fchange_to(self, obj: models.Order):
        if obj.change_to:
            return locale.currency(obj.change_to / 100, grouping=True)
        else:
            return None
    
    @admin.display(description=_("created"))
    def created_(self, obj):
        return obj.created.strftime("%d/%m/%Y %H:%M:%S")
    
    @admin.display(description=_("status"))
    def fstatus(self, obj):
        return format_html(
            '<span class="status {0}">{1}</span>',
            obj.status.code,
            obj.status.name
        )
       
    @admin.display(description=_("phone number"))
    def fphone(self, obj: models.Order):
        href = f"https://web.whatsapp.com/send/?phone=55{obj.phone}"
        phone = obj.fphone()
        return format_html(f'<a href="{href}" target="_blank">{phone}</a>')
    
    @admin.display(description=_("total"))
    def ftotal(self, obj: models.Order):
        style = "color: #07a607; font-weight: bold; font-size: 0.875rem;"
        return format_html(f'<span style="{style}">{obj.ftotal()}</span>')
            
    @admin.display(description=_("CEP"))
    def fcep(self, obj: models.Order):
        cep = f"{obj.logradouro_cep[0:5]}-{obj.logradouro_cep[5:]}"
        return cep

    def get_form(self, request, obj=None, **kwargs):
        if obj == None:
            kwargs["form"] = OrderForm
        
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly = []
        
        if obj == None:
            return readonly
        else:
            readonly.append("full_name")
            readonly.append("fphone")
            readonly.append("email")
            readonly.append("fcep")
            readonly.append("logradouro_name")
            if hasattr(obj, "address_complement") and getattr(obj, "address_complement") != None: 
                readonly.append("address_complement")
            if hasattr(obj, "address_number") and getattr(obj, "address_number") != None: 
                readonly.append("address_number")
            readonly.append("bairro_name")
            readonly.append("fstatus")
            if hasattr(obj, "fshipping_fee_value") and getattr(obj, "fshipping_fee_value") != None: 
                readonly.append("fshipping_fee_value")
            readonly.append("payment_type_name")
            if hasattr(self, "fchange_to") and getattr(self, "fchange_to")(obj) != None:
                readonly.append("fchange_to")
            if hasattr(self, "fchange_to") and getattr(self, "fchange_to")(obj) != None:
                readonly.append("fchange_to")
            readonly.append("created")
            readonly.append("received_date")
            readonly.append("ftotal")
                    
            return readonly
            
    def get_exclude(self, request, obj=None):
        exclude = [
            "user_request",
            "user_owner",
            "status",
            "address_complement",
            "address_number",
            "logradouro_cep",
            "uf_acronym",
            "shipping_fee_value",
            "total",
        ]
        
        if obj == None: 
            exclude.append("payment_type_name")
            exclude.append("created")
            exclude.append("received_date")
            exclude.append("total")
            
            return exclude
        else:
            exclude.append("payment_type")
            exclude.append("shipping_fee")
            exclude.append("change_to")
            exclude.append("phone")
            exclude.append("address")
            
            exclude_none = ["client"]
            for field in exclude_none:
                if field and getattr(obj, field) == None: 
                    exclude.append(field)
            
            return exclude
    
    def has_delete_permission(self, request, obj=None):
        return False
        
    def get_changeform_initial_data(self, request):
        user = request.user.owned_by if request.user.owned_by else request.user
        return {"user_owner": user}
    
    def save_model(self, request, obj, form, change):
        obj.user_owner = request.user.owned_by if request.user.owned_by else request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.owned_by if request.user.owned_by else request.user
        return qs.filter(user_owner=user)
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        
        try:
            extra_context["status"] = models.Status.objects.all().exclude(code="wating")
            extra_context["current_status"] = self.model.objects.get(id=object_id).status.code
        except ObjectDoesNotExist:
            extra_context["status"] = None
        
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )
        
    def response_change(self, request, obj: models.Order):
        if "status" in request.POST:
            status = request.POST.get("status")
            
            try:
                order_status = models.Status.objects.get(code=status)
                obj.status = order_status
                if status == "delivered":
                    obj.received_date = Now()
                obj.save()
            except ObjectDoesNotExist:
                pass
            return HttpResponseRedirect(request.get_full_path())
        return super().response_change(request, obj)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shipping_fee":
            kwargs["queryset"] = models.ShippingFee.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    class Media:
        js = ('js/pages/admin_order.js',)

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
        user = request.user.owned_by if request.user.owned_by else request.user
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

