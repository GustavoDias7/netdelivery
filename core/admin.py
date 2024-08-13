from django.contrib import admin
from . import models, forms
from core.utils import (first_occurrence, last_occurrence)
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render

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
    

class ShippingTaxAdmin(admin.ModelAdmin):
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
admin.site.register(models.Address)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ShippingTax, ShippingTaxAdmin)
admin.site.register(models.PaymentType, PaymentTypeAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.OrderItemStatus)

@admin.register(models.UF)
class UFAdmin(admin.ModelAdmin):
    readonly_fields = ("acronym",)
    
    
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
    search_fields = ("cep", "name")
    
    def import_action(self, request):
        context = {}
        
        if request.method == "POST":
            logradouros_file = request.FILES.get("logradouros")
            rows = []
            
            if logradouros_file:
                lines = logradouros_file.read().decode('latin1').splitlines()
                uf_acronym = lines[0].split("@")[1]
                    
                try:
                    uf = models.UF.objects.get(acronym=uf_acronym)
                except models.UF.DoesNotExist:
                    uf = None
                
                for line in lines:
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
    # list_display = ()
    readonly_fields = (
        "id",
        "name"
    )
    search_fields = ["name"]
    
    def import_action(self, request):
        context = {}
        ufs = models.UF.objects.all()
        context["ufs"] = ufs
        
        if request.method == "POST":
            bairros_file = request.FILES.get("bairros")
            uf = request.POST.get("uf")
            rows = []
            
            if bairros_file:
                lines = bairros_file.read().decode('latin1').splitlines()
                
                first = first_occurrence(lines, uf)
                last = last_occurrence(lines, uf)
                lines_by_uf = lines[first:last + 1]
                
                for line in lines_by_uf:
                    splitted = line.split("@")
                    rows.append(
                        models.Bairro(
                            id=splitted[0],
                            name=splitted[3],
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
    
    def import_action(self, request):
        context = {}
        ufs = models.UF.objects.all()
        context["ufs"] = ufs
        
        if request.method == "POST":
            localidades_file = request.FILES.get("localidades")
            uf = request.POST.get("uf")
            rows = []
            
            if localidades_file and uf:
                lines = localidades_file.read().decode('latin1').splitlines()
                
                first = first_occurrence(lines, uf)
                last = last_occurrence(lines, uf)
                lines_by_uf = lines[first:last + 1]
                
                for line in lines_by_uf:
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
