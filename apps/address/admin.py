from django.contrib import admin
from delivery.utils import (first_occurrence, last_occurrence, custom_titled_filter, create_temp_file)
from import_export.admin import ImportExportModelAdmin
from django.shortcuts import render
import chardet
from . import models
from django.conf import settings
import os
import pandas as pd
from os import listdir
from os.path import isfile, join

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        "user",
        "logradouro",
        "number",
        "complement"
    )
    
    def has_add_permission(self, request):
        return False
    
@admin.register(models.WhiteList)
class WhiteListAdmin(admin.ModelAdmin):
    filter_horizontal = ('ufs','localidades','bairros',)
    exclude = ("user",)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
    
    # def has_add_permission(self, request):
    #     return not self.model.objects.filter(user=request.user).exists()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        user = request.user.owned_by if request.user.owned_by else request.user
        qs = qs.filter(user=user)
        
        if request.method == "POST":
            acronyms = qs.first().ufs.values("id")
            qs_localidades = qs.first().localidades.filter(uf__id__in=acronyms)
            qs.first().localidades.set(qs_localidades)
            
            localidades = qs.first().localidades.values("id")
            qs_bairros = qs.first().bairros.filter(localidade__id__in=localidades)
            qs.first().bairros.set(qs_bairros)
        
        return qs
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "localidades":
            qs_whitelist = self.model.objects.filter(user=request.user)
            
            if len(qs_whitelist) > 0:
                acronyms = qs_whitelist.first().ufs.values("id")
                
                qs_localidades = models.Localidade.objects.filter(uf__id__in=acronyms)
                
                kwargs["queryset"] = qs_localidades
            else:
                kwargs["queryset"] = qs_whitelist
                
        if db_field.name == "bairros":
            qs_whitelist = self.model.objects.filter(user=request.user)
            
            if len(qs_whitelist) > 0:
                localidades_id = qs_whitelist.first().localidades.values("id")
                acronyms = qs_whitelist.first().ufs.values("id")
                
                qs_bairros = models.Bairro.objects.filter(
                    localidade__id__in=localidades_id,
                    localidade__uf__id__in=acronyms
                )
                
                kwargs["queryset"] = qs_bairros
            else:
                kwargs["queryset"] = qs_whitelist
                
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
@admin.register(models.UF)
class UFAdmin(admin.ModelAdmin):
    search_fields = ("acronym",)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
  
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
        "type",
        "name",
        "complement",
        "cep",
    )
    search_fields = ("cep", "type", "name", "localidade__name", "bairro__name")
    whitelist_bairros = None
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        
        is_client = request.GET.get('model_name') == 'client'
        if is_client:
            if not self.whitelist_bairros:
                self.whitelist_bairros = models.WhiteList.objects.all().first().bairros.values("id")
            queryset = queryset.filter(bairro__id__in=self.whitelist_bairros)
            
        return queryset, may_have_duplicates

    
    @admin.display(description='bairro')
    def bairro_(self, obj):
        return obj.bairro.name
    
    def import_action(self, request):
        context = {}
        
        folter = os.path.join(settings.BASE_DIR, "temp", "logradouros")
        
        if not os.path.exists(folter):
            os.makedirs(folter)
        
        if (len(listdir(folter))):
            files = [f for f in listdir(folter) if isfile(join(folter, f))]
            files.sort(key=lambda a : int(a.replace(".csv", "")))
            context["files"] = files
        
        logradouros_file = request.FILES.get("logradouros")
        if request.method == "POST" and logradouros_file:
            
            create_temp_file(logradouros_file, "logradouros.csv")
            
            file = os.path.join(settings.BASE_DIR, "temp", "logradouros.csv")
            
            reader = pd.read_csv(file, chunksize=3000, sep="@", encoding="ISO-8859-1")
            
            for i, chunk in enumerate(reader):
                chunk.to_csv(
                    os.path.join(settings.BASE_DIR, "temp", "logradouros", f'{i}.csv'),
                    sep="@",
                    index=False, 
                    header=["id","uf","localidade","bairro","bairro_init","name","complement","cep","type","ind_type","short_name"]
                )
                
            os.remove(file)
            
        elif request.method == "POST" and context.get("files"):
            file_name = context.get("files")[0]
            file_path = os.path.join(settings.BASE_DIR, "temp", "logradouros", file_name)
            reader = pd.read_csv(
                file_path, 
                chunksize=1000,
                sep="@",
                encoding='utf-8'
            )
            
            logradouros = []
            for i, chunk in enumerate(reader):
                for index, row in chunk.iterrows():
                    try:
                        uf = models.UF.objects.get(acronym=row.uf)
                    except models.UF.DoesNotExist:
                        uf = None
                    
                    try:
                        localidade = models.Localidade.objects.get(id=row.localidade)
                    except models.Localidade.DoesNotExist:
                        localidade = None
                    
                    try:
                        bairro = models.Bairro.objects.get(id=row.bairro)
                    except models.Bairro.DoesNotExist:
                        bairro = None
                    
                    logradouro = models.Logradouro(
                        id=row.id,
                        uf=uf,
                        localidade=localidade,
                        bairro=bairro,
                        name=row.get("name"),
                        complement=row.complement if type(row.complement) == str else None,
                        cep=row.cep,
                        type=row.type,
                    )
                    logradouros.append(logradouro)
            models.Logradouro.objects.bulk_create(logradouros)
            
            context["files"].pop(0)
            os.remove(file_path)
            
        return render(request, "admin/import_log.html", context)
        
@admin.register(models.Bairro)
class BairroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "localidade",
        "uf"
    )
    search_fields = ("name", "localidade__name", "localidade__uf__acronym")
    list_filter = [('localidade__name', custom_titled_filter('localidade'))]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        
        is_shippingfee = request.GET.get('model_name') == 'shippingfee'
        if is_shippingfee:
            qs_whitelist = models.WhiteList.objects.filter(user=request.user).first()
            whitelist_bairros = qs_whitelist.bairros.values("id")
            queryset = queryset.filter(id__in=whitelist_bairros)
        
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
    
    search_fields = ("id", "name", "cep")
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
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
