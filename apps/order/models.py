from django.db import models
from django.db.models.functions import Now
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.utils.translation import gettext_lazy as _
from apps.address.models import *
from apps.product.models import *
from apps.user.models import *
from netdelivery.utils import remove_non_numeric

import locale 

class Order(models.Model):
    user_owner = models.ForeignKey(User, verbose_name=_("user owner"), on_delete=models.PROTECT, related_name='user_owner')
    user_request = models.ForeignKey(User, verbose_name=_("user request"), null=True, blank=True, on_delete=models.SET_NULL, related_name='user_request')
    client = models.ForeignKey(Client, verbose_name=_("client"), null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey("Status", verbose_name=_("status"), on_delete=models.RESTRICT, default=1)
    payment_type = models.ForeignKey("PaymentType", verbose_name=_("payment type"), on_delete=models.RESTRICT)
    payment_type_name = models.CharField(_("payment type name"), max_length=30)
    change_to = models.PositiveSmallIntegerField(_("change to"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    shipping_fee = models.ForeignKey("ShippingFee", verbose_name=_("shipping fee"), on_delete=models.RESTRICT, null=True)
    shipping_fee_value = models.PositiveSmallIntegerField(_("shipping fee value"), null=True, validators=[MaxValueValidator(32767)])
    created = models.DateTimeField(_("created"), null=True, blank=True, db_default=Now())
    received_date = models.DateTimeField(_("received date"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        
    def save(self, *args, **kwargs):
        self.payment_type_name = self.payment_type.name
        if self.shipping_fee:
            self.shipping_fee_value = self.shipping_fee.value
        super(Order, self).save(*args, **kwargs)
    
    def fshipping_fee_value(self):
        if self.shipping_fee_value:
            float_value = self.shipping_fee_value / 100
            formatted_value = locale.currency(float_value, grouping=True)
            return formatted_value
        else:
            return self.shipping_fee_value
    
    def setShippingFee(self, sf):
        self.shipping_fee = sf
        self.shipping_fee_value = sf.value
        
    def setPaymentType(self, pt):
        self.payment_type = pt
        self.payment_type_name = pt.name
        
    def __str__(self):
        return f"{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", verbose_name=_("order"), on_delete=models.RESTRICT)
    product = models.ForeignKey(ProductVariant, verbose_name=_("product"), null=True, blank=True, on_delete=models.SET_NULL)
    combo = models.ForeignKey(Combo, verbose_name=_("combo"), null=True, blank=True, on_delete=models.RESTRICT)
    product_name = models.CharField(verbose_name=_("product name"), null=True, blank=True, max_length=100)
    price = models.PositiveIntegerField(verbose_name=_("price"), null=True, blank=True, validators=[MaxValueValidator(2147483647)])
    discount = models.DecimalField(
        verbose_name=_("discount"), 
        null=True, blank=True,
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=_("quantity"), validators=[MaxValueValidator(32767)])
    
    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        
    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
            self.discount = self.product.discount
            self.product_name = self.product.full_name()
            self.combo = None
        elif self.combo:
            self.price = self.combo.price
            self.discount = self.combo.discount
            self.product_name = self.combo.name
            self.product = None
            
        super(OrderItem, self).save(*args, **kwargs)
    
    def percentage_discount(self):
        percentage = int(float(self.discount) * 100)
        return percentage
    
    def fpercentage_discount(self):
        return f"{self.percentage_discount()}%"
    
    def fprice(self):
        return locale.currency(self.price / 100, grouping=True)
    
    def ftotal_price(self):
        disc = float(self.discount * self.quantity) * self.price
        fee = self.order.shipping_fee_value if self.order.shipping_fee_value != None else 0
        total = ((self.price * self.quantity) - disc) + fee
        formatted_total = locale.currency(total / 100, grouping=True)
        return formatted_total
    
    def fquantity(self):
        units = f"{self.quantity} unidades"
        unit = f"{self.quantity} unidade"
        return units if self.quantity > 1 else unit
    
    def __str__(self):
        return f"{self.id}"
    
class Status(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=30)
    code = models.CharField(verbose_name=_("code"), max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("status")
    
    def __str__(self):
        return f"{self.name}"

class PaymentType(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=30)
    code = models.CharField(verbose_name=_("code"), max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("payment type")
        verbose_name_plural = _("payment types")
    
    def __str__(self):
        return f"{self.name}"

class ShippingFee(models.Model):
    user = models.ForeignKey("user.User", verbose_name=_("user"), null=True, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(verbose_name=_("value"), validators=[MaxValueValidator(32767)])
    bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(verbose_name=_("default"), default=False)
    
    class Meta:
        verbose_name = _("shipping fee")
        verbose_name_plural = _("shipping fees")
        unique_together = ('bairro', 'user',)
        
    def clean_fields(self, exclude=None):
        if self.value and type(self.value) == str:
            self.value = int(remove_non_numeric(self.value))
        super().clean_fields(exclude=exclude)
        
    def fvalue(self):
        float_value = self.value / 100
        formatted_value = locale.currency(float_value, grouping=True)
        return formatted_value
    
    def __str__(self):
        if self.bairro:
            return f"{self.bairro.name}: {self.fvalue()}"
        elif self.is_default:
            return f"{_('default')}: {self.fvalue()}"
        else:
            return f"{_('shipping fee')} {self.id}"
