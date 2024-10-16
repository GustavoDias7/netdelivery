from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
# from django.core import validators
# from core.validators import (cep_validator, name_validator, phone_validator)
# from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# import locale 

# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)])
#     # image = models.ImageField()
#     description = models.TextField(max_length=400, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
#     stock = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483647)])
#     # stock == null/None == unlimited
#     archived = models.BooleanField(default=False)
#     discount = models.DecimalField(
#         max_digits=3,
#         decimal_places=2,
#         default=0.0,
#         validators=[MinValueValidator(0), MaxValueValidator(1)],
#     )
#     product_category = models.ForeignKey("ProductCategory", on_delete=models.RESTRICT)
    
#     def fprice(self):
#         return locale.currency(self.price / 100, grouping=True)

#     def __str__(self):
#         return f"{self.name}"
    
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        max_length=400, 
        validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))]
    )
    # image = models.ImageField()
    
    def __str__(self):
        return f"{self.name}"
    
class PizzaVariant(models.Model):
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    size_name = models.CharField(max_length=40, help_text=_("Ex.: Pequena, Média, Grande"))
    short_size_name = models.CharField(blank=True, null=True, max_length=5, help_text=_("Opcional. Ex.: P, M, G"))
    diameter = models.PositiveSmallIntegerField(validators=[MaxValueValidator(32767)], help_text=_("Em centimetros"))
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)], help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99"))
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    stock = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483647)], help_text=_("Opcional. Se não for preenchido, o estoque será ilimitado para pedidos. 0 representa que o estoque está vazio."))
    stuffed_edge = models.BooleanField(default=True)
    archived = models.BooleanField(default=True)
    default = models.BooleanField(default=False, help_text=_("A variante que representará a pizza e será mostrada no site. Se não houver uma variante padrão a primeira variante registrada será mostrada no site. Se existir duas ou mais variantes padrões a primeira variante registrada e marcada como padrão será mostrada no site."))
    
    class Meta:
        verbose_name = _("Variante de pizza")
        verbose_name_plural = _("Variantes de pizza")
        
    def __str__(self):
        return f"{self.pizza.name} {self.size_name}"
    
class Soda(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        max_length=400, 
        validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))]
    )
    # image = models.ImageField()
    
    class Meta:
        verbose_name = _("Refrigerante")
        verbose_name_plural = _("Refrigerantes")
    
    def __str__(self):
        return f"{self.name}"

class SodaVariant(models.Model):
    soda = models.ForeignKey("Soda", on_delete=models.CASCADE)
    measure = models.CharField(max_length=40, help_text=_("Ex.: 2 Litros, 2L, 250ml"))
    price = models.PositiveIntegerField(
        validators=[MaxValueValidator(2147483647)], 
        help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99")
    )
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    stock = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        validators=[MaxValueValidator(2147483647)], 
        help_text=_("Opcional. Se não for preenchido, o estoque será ilimitado para pedidos. 0 representa que o estoque está vazio.")
    )
    archived = models.BooleanField(default=True)
    default = models.BooleanField(
        default=False, 
        help_text=_("A variante que representará o refrigerante e será mostrada no site. Se não houver uma variante padrão a primeira variante registrada será mostrada no site. Se existir duas ou mais variantes padrões a primeira variante registrada e marcada como padrão será mostrada no site.")
    )
    
    class Meta:
        verbose_name = _("Variante de refrigerante")
        verbose_name_plural = _("Variantes de refrigerante")
        
    def __str__(self):
        return f"{self.soda.name} {self.measure}"
    
# class ProductCategory(models.Model):
#     name = models.CharField(max_length=30)
#     code = models.CharField(max_length=30, unique=True)
    
#     class Meta:
#         verbose_name = _("Product Category")
#         verbose_name_plural = _("Product Categories")

#     def __str__(self):
#         return f"{self.name}"