from django.db import models
from apps.core.validators import (cep_validator)
from django.core.validators import (MaxValueValidator, MinLengthValidator)
from django.utils.translation import gettext_lazy as _

class Address(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    logradouro = models.ForeignKey("Logradouro", on_delete=models.RESTRICT, null=True)
    number = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(32767)]) 
    complement = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
    
    def get(self, name):
        return getattr(self, name)
    
    def set(self, name, value):
        setattr(self, name, value)
        
    def setLog(self, log):
        self.logradouro = log
        self.number = None
        self.complement = log.complement if log.complement else None
        self.order_address = None
        
    def is_equal(self, key, value):
        result = False
        
        match key:
            case "cep":
                result = self.logradouro.cep == value
            case "number": 
                result = self.number == value
            case "complement":
                result = self.complement == value
            case _:
                pass
            
        return result
        
    
    def __str__(self):
        return f"{self.logradouro.type} {self.logradouro.name}"

class Logradouro(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    uf = models.ForeignKey("UF", on_delete=models.RESTRICT)
    localidade = models.ForeignKey("Localidade", null=True, on_delete=models.SET_NULL)
    bairro = models.ForeignKey("Bairro", null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    complement = models.CharField(null=True, max_length=100)
    cep = models.CharField(max_length=8, validators=[cep_validator])
    type = models.CharField(max_length=36)
        
    def fcep(self):
        if len(self.cep):
            return f"{self.cep[0:5]}-{self.cep[5:]}"
        else:
            return self.cep
    
    def select2(self):
        return f"{self.cep}, {self.type} {self.name}, {self.bairro.name} ({self.localidade} - {self.uf})"
    
    def __str__(self):
        return f"{self.type} {self.name}"
    
class UF(models.Model):
    acronym = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    
    def __str__(self):
        return f"{self.acronym}"

class Bairro(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=72)
    localidade = models.ForeignKey("Localidade", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.name and self.localidade:
            return f"{self.name} ({self.localidade.name} - {self.localidade.uf.acronym})"
        else:
            return self.name
    
class Localidade(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    uf = models.ForeignKey("UF", on_delete=models.SET_NULL, null=True)
    situacaolocalidade = models.ForeignKey("SituacaoLocalidade", on_delete=models.RESTRICT, null=True)
    tipolocalidade = models.ForeignKey("TipoLocalidade", on_delete=models.RESTRICT)
    name = models.CharField(max_length=72)
    cep = models.CharField(max_length=8, validators=[cep_validator])
    
    def __str__(self):
        return f"{self.name}"
    
class SituacaoLocalidade(models.Model):
    definition = models.TextField(max_length=60)
    
    def __str__(self):
        return f"Situação {self.id}"
    
class TipoLocalidade(models.Model):
    code = models.CharField(max_length=1)
    definition = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.code} - {self.definition}"
  
class WhiteList(models.Model):
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)
    ufs = models.ManyToManyField(UF, blank=True)
    localidades = models.ManyToManyField(Localidade, blank=True)
    bairros = models.ManyToManyField(Bairro, blank=True)

    class Meta:
        verbose_name = _("whiteList")
        verbose_name_plural = _("whiteLists")
    
    def __str__(self):
        return f"WhiteList {self.id}"
  