from django.db import models
from django.db.models.functions import Now
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.utils.translation import gettext_lazy as _
from apps.core.validators import cep_validator
from apps.address.models import *
from apps.product.models import *
from apps.user.models import *

import locale 

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

class Order(models.Model):
    user_owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_owner')
    user_request = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_request')
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    payment_type = models.ForeignKey("PaymentType", on_delete=models.RESTRICT)
    payment_type_name = models.CharField(max_length=30)
    payment_type_code = models.CharField(max_length=30)
    shipping_fee = models.ForeignKey("ShippingFee", on_delete=models.RESTRICT, null=True)
    shipping_fee_value = models.PositiveSmallIntegerField(null=True, validators=[MaxValueValidator(32767)])
    created = models.DateTimeField(db_default=Now())
    received_date = models.DateTimeField(null=True, blank=True)
        
    def save(self, *args, **kwargs):
        self.payment_type_name = self.payment_type.name
        self.payment_type_code = self.payment_type.code
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
        self.payment_type_code = pt.code
        
    def __str__(self):
        return f"{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.RESTRICT)
    order_item_status = models.ForeignKey("OrderItemStatus", on_delete=models.RESTRICT, default=1)
    product = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    combo = models.ForeignKey(Combo, null=True, blank=True, on_delete=models.RESTRICT)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)])
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(32767)])
    
    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")
        
    def save(self, *args, **kwargs):
        if self.product:
            self.price = self.product.price
            self.discount = self.product.discount
            self.combo = None
        elif self.combo:
            self.price = self.combo.price
            self.discount = self.combo.discount
            self.product = None
            
        super(OrderItem, self).save(*args, **kwargs)
    
    def percentage_discount(self):
        percentage = int(float(self.discount) * 100)
        return percentage
    
    def fpercentage_discount(self):
        return f"{self.percentage_discount()}%"
    
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
    
class OrderItemStatus(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("Order item status")
        verbose_name_plural = _("Order item status")
    
    def __str__(self):
        return f"{self.name}"

class PaymentType(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return f"{self.name}"

class ShippingFee(models.Model):
    user = models.ForeignKey("user.User", null=True, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(32767)])
    bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(_('Default'), default=False)
    
    class Meta:
        verbose_name = _("Shipping fee")
        verbose_name_plural = _("Shipping fees")
        unique_together = ('bairro', 'user',)
        
    def fvalue(self):
        float_value = self.value / 100
        formatted_value = locale.currency(float_value, grouping=True)
        return formatted_value
    
    def __str__(self):
        if self.bairro:
            return f"{self.bairro.name}"
        elif self.is_default:
            return f"{_('default')}"
        else:
            return f"ShippingFee {self.id}"

# class OrderAddress(models.Model):
#     address_number = models.PositiveSmallIntegerField(_("Number"), blank=True, null=True, validators=[MaxValueValidator(32767)]) 
#     address_complement = models.CharField(_("Complement"), max_length=100, blank=True, null=True)
#     uf_acronym = models.CharField("UF", max_length=2, validators=[MinLengthValidator(2)])
#     logradouro_cep = models.CharField("CEP", max_length=8, validators=[cep_validator])
#     logradouro_name = models.CharField("Nome do logradouro", max_length=100)
#     logradouro_type = models.CharField("Tipo do logradouro", max_length=36)
#     localidade_name = models.CharField("Localidade", max_length=72)
#     bairro_name = models.CharField("Bairro", max_length=72)
    
#     def set(self, addr):
#         self.address_number = addr.number
#         self.address_complement = addr.complement
#         self.uf_acronym = addr.logradouro.uf.acronym
#         self.logradouro_cep = addr.logradouro.cep
#         self.logradouro_name = addr.logradouro.name
#         self.logradouro_type = addr.logradouro.type
#         self.localidade_name = addr.logradouro.localidade.name
#         self.bairro_name = addr.logradouro.bairro.name
    
#     def __str__(self):
#         return f"{self.logradouro_type} {self.logradouro_name}, {self.localidade_name} - {self.uf_acronym}"
