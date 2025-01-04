from urllib.parse import urlencode
from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.utils.translation import gettext_lazy as _
import locale 
from django.template.defaultfilters import slugify
from delivery.utils import remove_non_numeric
from delivery.constants import PIZZA_SIZES

class Category(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
    
    def get_code(self):
        return slugify(self.name)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    user = models.ForeignKey("user.User", verbose_name=_("user"), null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("name"), max_length=100)
    image = models.ImageField(verbose_name=_("image"))
    description = models.TextField(verbose_name=_("description"), max_length=600, validators=[MinLengthValidator(4, _("Minimum of 4 characters."))])
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
    
    def __str__(self):
        return f"{self.name}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey("Product", verbose_name=_("product"), on_delete=models.CASCADE)
    size = models.CharField(verbose_name=_("size"), max_length=40, blank=True, null=True, choices=PIZZA_SIZES)
    diameter = models.PositiveSmallIntegerField(verbose_name=_("diameter"), blank=True, null=True, validators=[MaxValueValidator(32767)], help_text=_("In centimeters"))
    stuffed_edge = models.BooleanField(verbose_name=_("stuffed edge"), blank=True, null=True, choices=[(None, "Sem borda"), (True, "Sim"), (False, "Não")])
    milliliters = models.PositiveSmallIntegerField(verbose_name=_("milliliters"), blank=True, null=True, validators=[MaxValueValidator(32767)])
    price = models.PositiveIntegerField(verbose_name=_("price"), validators=[MaxValueValidator(2147483647)])
    discount = models.DecimalField(
        verbose_name=_("discount"), 
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_("In decimal. Ex.: 0.1 to represent 10%. 0.0 when there is no discount.")
    )
    stock = models.PositiveIntegerField(verbose_name=_("stock"), blank=True, null=True, validators=[MaxValueValidator(2147483647)], help_text=_("Optional. If left blank, stock will be unlimited for orders. 0 represents that stock is empty."))
    archived = models.BooleanField(verbose_name=_("archived"), default=False)
    default = models.BooleanField(verbose_name=_("default"), default=False, help_text=_("The variant that will represent the product on the website."))
    
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
    user = models.ForeignKey("user.User", verbose_name=_("user"), null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("name"), max_length=100)
    image = models.ImageField(verbose_name=_("image"))
    description = models.TextField(verbose_name=_("description"), max_length=400, validators=[MinLengthValidator(4, _("Minimum of 4 characters."))])
    price = models.PositiveIntegerField(verbose_name=_("price"), validators=[MaxValueValidator(2147483647)])
    discount = models.DecimalField(
        verbose_name=_("discount"), 
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_("In decimal. Ex.: 0.1 to represent 10%. 0.0 when there is no discount.")
    )
    archived = models.BooleanField(verbose_name=_("archived"), default=False)
    
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
    combo = models.ForeignKey("Combo", verbose_name=_("combo"), on_delete=models.CASCADE)
    product_variant = models.ForeignKey("ProductVariant", verbose_name=_("product variant"), null=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = _("combo item")
        verbose_name_plural = _("combo items")
    
    def __str__(self):
        if self.product_variant.product:
            return f"{self.product_variant.product.name}"
        else:
            return ""