from urllib.parse import urlencode
from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.utils.translation import gettext_lazy as _
import locale 
from django.template.defaultfilters import slugify
from delivery.utils import remove_non_numeric
from delivery.constants import PIZZA_SIZES

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
    
    def get_code(self):
        return slugify(self.name)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    user = models.ForeignKey("user.User", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(max_length=600, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
    
    def __str__(self):
        return f"{self.name}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size = models.CharField(_("Size"), max_length=40, blank=True, null=True, choices=PIZZA_SIZES)
    diameter = models.PositiveSmallIntegerField(_("Diameter"), blank=True, null=True, validators=[MaxValueValidator(32767)], help_text=_("Em centimetros"))
    stuffed_edge = models.BooleanField(_("Stuffed Edge"), blank=True, null=True, choices=[(None, "Sem borda"), (True, "Sim"), (False, "Não")])
    milliliters = models.PositiveSmallIntegerField(_("Milliliters"), blank=True, null=True, validators=[MaxValueValidator(32767)])
    price = models.PositiveIntegerField(_("Price"), validators=[MaxValueValidator(2147483647)], help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99"))
    discount = models.DecimalField(
        _("Discount"),
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    stock = models.PositiveIntegerField(_("Stock"), blank=True, null=True, validators=[MaxValueValidator(2147483647)], help_text=_("Opcional. Se não for preenchido, o estoque será ilimitado para pedidos. 0 representa que o estoque está vazio."))
    archived = models.BooleanField(_("Archived"), default=False)
    default = models.BooleanField(_("Default"), default=False, help_text=_("A variante que representará o produto no site."))
    
    class Meta:
        verbose_name = _("product variant")
        verbose_name_plural = _("product variants")
        
    def clean_fields(self, exclude=None):
        if self.price and type(self.price) == str:
            self.price = int(remove_non_numeric(self.price))
        super().clean_fields(exclude=exclude)
        
    def fsize(self):
        if self.size:
            return PIZZA_SIZES[self.size]
        else:
            return None
        
    def fmilliliters(self):
        if self.milliliters:
            if self.milliliters < 1000:
                return "{} ml".format(self.milliliters)
            else:
                liter = self.milliliters / 1000
                result = str(int(liter)) if liter.is_integer() else str(liter).replace(".", ",")
                return "{} L".format(result)
        else:
            return self.milliliters
            
    
    def fprice(self):
        return locale.currency(self.price / 100, grouping=True)
    
    def fdiscount(self):
        return f"-{int(self.discount * 100)}%"
    
    def total(self):
        return int(self.price - self.price * self.discount)
        
    def ftotal(self):
        total = self.total()
        return locale.currency(total / 100, grouping=True)

    def link(self):
        params = {"id": self.product.id, "variant": self.id}
        query_string = urlencode(params)
        return f"/{self.product.user.username}/produto?{query_string}" 
    
    def full_name(self):
        if self.size:
            return f"{self.product.name} {PIZZA_SIZES[self.size]}"
        elif self.milliliters:
            return f"{self.product.name} {self.fmilliliters()}"
        else:
            return self.product.name
        
    def __str__(self):
        return self.full_name()

    
class Combo(models.Model):
    user = models.ForeignKey("user.User", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(max_length=400, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)], help_text=_("Em inteiro. Ex.: 4999 para representar R$ 49,99"))
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Em decimal. Ex.: 0.1 para representar 10%. 0.0 quando não há desconto."
    )
    archived = models.BooleanField(default=True)
    
    def clean_fields(self, exclude=None):
        if self.price and type(self.price) == str:
            self.price = int(remove_non_numeric(self.price))
        super().clean_fields(exclude=exclude)
    
    def fprice(self):
        return locale.currency(self.price / 100, grouping=True)
    
    def fdiscount(self):
        return f"-{int(self.discount * 100)}%"
    
    def total(self):
        return int(self.price - self.price * self.discount)
        
    def ftotal(self):
        total = self.total()
        return locale.currency(total / 100, grouping=True)

    def link(self):
        params = {"id": self.id}
        query_string = urlencode(params)
        return f"/{self.user.username}/combo?{query_string}" 
    
    def __str__(self):
        return f"{self.name}"
    
class ComboItem(models.Model):
    combo = models.ForeignKey("Combo", on_delete=models.CASCADE)
    product_variant = models.ForeignKey("ProductVariant", null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        if self.product_variant.product:
            return f"{self.product_variant.product.name}"
        else:
            return ""