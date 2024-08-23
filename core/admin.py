from django.contrib import admin
from . import models
from core.utils import (first_occurrence, last_occurrence, custom_titled_filter)
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render
import chardet
from django.utils.translation import gettext_lazy as _

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
    

class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "id"]
    
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    
class OrderAdmin(admin.ModelAdmin):
    # list_display = []
    readonly_fields = []
    
    # def get_readonly_fields(self, request, obj=None):
    #     return list(self.readonly_fields) + \
    #         [field.name for field in obj._meta.fields] + \
    #         [field.name for field in obj._meta.many_to_many]
    
class OrderItemAdmin(admin.ModelAdmin):
    # list_display = []
    readonly_fields = []
    
admin.site.register(models.User)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.PaymentType, PaymentTypeAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.OrderItemStatus)

@admin.register(models.ShippingFee)
class ShippingFeeAdmin(admin.ModelAdmin):
    list_display = ("bairro_", "value", "is_default")
    autocomplete_fields = ("bairro",)
    
    @admin.display(empty_value=_("Default"))
    def bairro_(self, obj):
        return obj.bairro

@admin.register(models.UF)
class UFAdmin(admin.ModelAdmin):
    search_fields = ("acronym",)
    readonly_fields = ("acronym",)
    
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        "user",
        "logradouro",
        "number",
        "complement"
    )
    
@admin.register(models.Logradouro)
class LogradouroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        "id",
        "uf",
        "bairro",
        "localidade",
        "name",
        "complement",
        "cep",
        "type"
    )
    readonly_fields = list_display
    search_fields = ("cep", "name", "bairro__name")
    
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
        "localidade"
    )
    readonly_fields = list_display
    search_fields = ["id", "name"]
    list_filter = [('localidade__name', custom_titled_filter('localidade'))]
    
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
        "name",
        "cep",
    )
    readonly_fields = (
        "id",
        "situacaolocalidade",
        "tipolocalidade",
        "name",
        "cep",
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
                    
                    if sit_localidade and tipo_localidade:
                        rows.append(
                            models.Localidade(
                                id=splitted[0],
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
    list_display = ("bairro",)
    autocomplete_fields = ("bairro",)