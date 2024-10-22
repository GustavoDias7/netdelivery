from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.utils.translation import gettext_lazy as _
import locale 

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField()
    description = models.TextField(max_length=400, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
    product_category = models.ForeignKey("ProductCategory", on_delete=models.RESTRICT)
    combo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")

    def __str__(self):
        return f"{self.name}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size_name = models.CharField(max_length=40, help_text=_("Ex.: Pequena, Média, Grande, 2l, 200ml"))
    short_size_name = models.CharField(blank=True, null=True, max_length=5, help_text=_("Opcional. Ex.: P, M, G"))
    diameter = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(32767)], help_text=_("Em centimetros"))
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)], help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99"))
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    stock = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483647)], help_text=_("Opcional. Se não for preenchido, o estoque será ilimitado para pedidos. 0 representa que o estoque está vazio."))
    stuffed_edge = models.BooleanField(blank=True, null=True, choices=[(None, "Sem borda"), (True, "Sim"), (False, "Não")])
    archived = models.BooleanField(default=True)
    default = models.BooleanField(default=False, help_text=_("A variante que representará o produto no site."))
    
    class Meta:
        verbose_name = _("Variante do produto")
        verbose_name_plural = _("Variantes do produto")
    
    def fprice(self):
        return locale.currency(self.price / 100, grouping=True)
        
    def __str__(self):
        return f"{self.product.name} {self.size_name}"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=30)
    code = models.SlugField(max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return f"{self.name}"
    
class Combo(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField()
    description = models.TextField(max_length=400, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)], help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99"))
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    
    def __str__(self):
        return f"{self.name}"
    
class ComboItem(models.Model):
    combo = models.ForeignKey("Combo", on_delete=models.CASCADE)
    product_variant = models.ForeignKey("ProductVariant", on_delete=models.CASCADE)