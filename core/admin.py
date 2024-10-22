from django.contrib import admin
from . import models
from core.utils import (first_occurrence, last_occurrence, custom_titled_filter)
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render
import chardet
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

class CustomAutocompleteJsonView(AutocompleteJsonView):
    def serialize_result(self, obj, to_field_name):
        text = str(obj.autocomplete() if obj.autocomplete else obj)
        return {'id': str(getattr(obj, to_field_name)), 'text': text}  

def autocomplete_view(self, request):
    return CustomAutocompleteJsonView.as_view(admin_site=self)(request)

@admin.register(models.PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    add_fieldsets = ((
        None, 
        { 'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}
    ))

admin.site.register(models.OrderItemStatus)

class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    readonly_fields = (
        "price",
        "discount",
    )
    
@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "logradouro", "phone", "cpf")
    search_fields = ("full_name", "logradouro__cep", "logradouro__name", "phone", "cpf")
    autocomplete_fields = ("logradouro",)
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "client",
        "payment_type",
        "shipping_fee",
        "shipping_fee_value",
        "created",
        "received_date",
    )
    readonly_fields = (
        "payment_type_name",
        "payment_type_code",
        "shipping_fee_value",
        "created",
    )
    autocomplete_fields = ("client",)
    def save_model(self, request, obj, form, change):
        self.model.payment_type_name = "Test"
        super().save_model(request, obj, form, change)

@admin.register(models.ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "uf", "localidade", "value", "is_default")
    autocomplete_fields = ("whitelistbairro",)
    
    @admin.display(empty_value=_("Default"))
    def bairro_(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.name
    
    @admin.display(description='Localidade')
    def localidade(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.localidade.name
        else:
            return "-"
        
    @admin.display(description='uf')
    def uf(self, obj):
        if obj.whitelistbairro:
            return obj.whitelistbairro.bairro.localidade.uf.acronym
        else:
            return "-"

@admin.register(models.UF)
class UFAdmin(admin.ModelAdmin):
    search_fields = ("acronym",)
    readonly_fields = ("acronym",)
    
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        "order_address",
        "user",
        "logradouro",
        "number",
        "complement"
    )
    
@admin.register(models.OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "address_number",
        "address_complement",
        "uf_acronym",
        "logradouro_cep",
        "logradouro_name",
        "logradouro_type",
        "localidade_name",
        "bairro_name",
    )
    
@admin.register(models.Logradouro)
class LogradouroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        "id",
        "uf",
        "bairro_",
        "localidade",
        "name",
        "complement",
        "cep",
        "type"
    )
    readonly_fields = (
        "id",
        "uf",
        "bairro",
        "localidade",
        "name",
        "complement",
        "cep",
        "type"
    )
    search_fields = ("cep", "type", "name", "localidade__name", "bairro__name")
    wl_bairros = models.WhiteListBairro.objects.all()
    
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        
        if request.GET.get('model_name') == 'client':
            queryset = queryset.filter(bairro__in=self.wl_bairros.values_list("bairro"))
            
        return queryset, may_have_duplicates

    
    @admin.display(description='bairro')
    def bairro_(self, obj):
        return obj.bairro.name
        
    def import_action(self, request):
        context = {}
        
        if request.method == "POST":
            logradouros_file = request.FILES.get("logradouros")
            rows = []
            
            if logradouros_file:
                
                file = logradouros_file.read()
                file_detected = chardet.detect(file)
                decoded = file.decode(file_detected['encoding']).splitlines()
                
                uf_acronym = decoded[0].split("@")[1]
                    
                try:
                    uf = models.UF.objects.get(acronym=uf_acronym)
                except models.UF.DoesNotExist:
                    uf = None
                
                for line in decoded:
                    splitted = line.split("@")
                    try:
                        localidade = models.Localidade.objects.get(id=splitted[2])
                    except models.Localidade.DoesNotExist:
                        localidade = None
                    
                    try:
                        bairro = models.Bairro.objects.get(id=splitted[3])
                    except models.Bairro.DoesNotExist:
                        bairro = None
                    
                    if uf and localidade and bairro:
                        logradouro = models.Logradouro(
                            id=splitted[0],
                            uf=uf,
                            localidade=localidade,
                            bairro=bairro,
                            name=splitted[5],
                            complement=splitted[6],
                            cep=splitted[7],
                            type=splitted[8],
                        )
                        rows.append(logradouro)
                
                models.Logradouro.objects.bulk_create(rows)
                
        return render(request, "admin/import_log.html", context)

@admin.register(models.Bairro)
class BairroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "localidade",
        "uf"
    )
    readonly_fields = (
        "id",
        "name",
        "localidade",
    )
    search_fields = ("name", "localidade__name", "localidade__uf__acronym")
    list_filter = [('localidade__name', custom_titled_filter('localidade'))]
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        queryset = queryset.all()

        return queryset, use_distinct
    
    @admin.display(description='uf')
    def uf(self, obj):
        if obj.localidade: return obj.localidade.uf.acronym
        else: return "-"
            
    
    def import_action(self, request):
        context = {}
        ufs = models.UF.objects.all()
        context["ufs"] = ufs
        
        if request.method == "POST":
            bairros_file = request.FILES.get("bairros")
            uf = request.POST.get("uf")
            rows = []
            
            if bairros_file:
                file = bairros_file.read()
                file_detected = chardet.detect(file)
                decoded = file.decode(file_detected['encoding']).splitlines()
                
                first = first_occurrence(decoded, uf)
                last = last_occurrence(decoded, uf)
                lines = decoded[first:last + 1]
                
                for line in lines:
                    splitted = line.split("@")
                    
                    try:
                        loc = models.Localidade.objects.get(id=splitted[2])
                    except:
                        loc = None
                        
                    rows.append(
                        models.Bairro(
                            id=splitted[0],
                            name=splitted[3],
                            localidade=loc
                        )
                    )
                    
                models.Bairro.objects.bulk_create(rows)
            
        return render(request, "admin/import_bairro.html", context)

@admin.register(models.Localidade)
class LocalidadeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        "id",
        "uf",
        "name",
        "cep",
    )
    readonly_fields = (
        "id",
        "situacaolocalidade",
        "tipolocalidade",
        "name",
        "cep",
        "uf",
    )
    
    search_fields = ["id", "name", "cep"]
    
    def import_action(self, request):
        context = {}
        ufs = models.UF.objects.all()
        context["ufs"] = ufs
        
        if request.method == "POST":
            localidades_file = request.FILES.get("localidades")
            uf = request.POST.get("uf")
            rows = []
            
            if localidades_file and uf:
                file = localidades_file.read()
                file_detected = chardet.detect(file)
                decoded = file.decode(file_detected['encoding']).splitlines()
                
                first = first_occurrence(decoded, uf)
                last = last_occurrence(decoded, uf)
                lines = decoded[first:last + 1]
                
                for line in lines:
                    splitted = line.split("@")
                    try:
                        if splitted[4]:
                            sit_localidade = models.SituacaoLocalidade.objects.get(id=splitted[4])
                        else:
                            sit_localidade = None
                    except models.SituacaoLocalidade.DoesNotExist:
                        sit_localidade = None
                    
                    try:
                        tipo_localidade = models.TipoLocalidade.objects.get(code=splitted[5])
                    except models.TipoLocalidade.DoesNotExist:
                        tipo_localidade = None
                    
                    try:
                        uf = models.UF.objects.get(acronym=splitted[1])
                    except models.UF.DoesNotExist:
                        uf = None
                    
                    if sit_localidade and tipo_localidade and uf:
                        rows.append(
                            models.Localidade(
                                id=splitted[0],
                                uf=uf,
                                situacaolocalidade=sit_localidade,
                                tipolocalidade=tipo_localidade,
                                name=splitted[2],
                                cep=splitted[3],
                            )
                        )
                    
                models.Localidade.objects.bulk_create(rows)
            
        return render(request, "admin/import_loc.html", context)

@admin.register(models.WhiteListUF)
class WhiteListUFAdmin(admin.ModelAdmin):
    list_display = ("uf",)
    autocomplete_fields = ("uf",)
    
@admin.register(models.WhiteListLocalidade)
class WhiteListLocalidadeAdmin(admin.ModelAdmin):
    list_display = ("localidade",)
    autocomplete_fields = ("localidade",)
    
@admin.register(models.WhiteListBairro)
class WhiteListBairroAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "localidade", "uf")
    search_fields = ("bairro",)
    autocomplete_fields = ("bairro",)
    
    @admin.display(description='bairro')
    def bairro_(self, obj):
        return obj.bairro.name
    
    @admin.display(description='localidade')
    def localidade(self, obj):
        return obj.bairro.localidade.name
        
    @admin.display(description='uf')
    def uf(self, obj):
        return obj.bairro.localidade.uf.acronym