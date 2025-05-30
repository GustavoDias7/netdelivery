from django.db import models
from django.db.models.functions import Now
from django.db.models import QuerySet
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.utils.translation import gettext_lazy as _
from apps.address.models import *
from apps.product.models import *
from apps.user.models import *
from delivery.utils import remove_non_numeric

import locale 

class Order(models.Model):
    user_owner = models.ForeignKey(User, verbose_name=_("user owner"), on_delete=models.PROTECT, related_name='user_owner')
    
    # user    
    user_request = models.ForeignKey(User, verbose_name=_("user request"), null=True, blank=True, on_delete=models.SET_NULL, related_name='user_request')
    client = models.ForeignKey(Client, verbose_name=_("client"), null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(verbose_name=_("full name"), max_length=60)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(verbose_name=_("phone number"), max_length=11, null=True, blank=True, validators=[phone_validator])
    
    # address
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True)
    address_number = models.PositiveSmallIntegerField(_("number"), blank=True, null=True, validators=[MaxValueValidator(32767)]) 
    address_complement = models.CharField(_("complement"), max_length=100, blank=True, null=True)
    logradouro_name = models.CharField(_("address"), max_length=100) # logradouro.fullname()
    logradouro_cep = models.CharField(_("cep"), max_length=8, validators=[cep_validator])
    uf_acronym = models.CharField(_("state"), max_length=2, validators=[MinLengthValidator(2)])
    bairro_name = models.CharField(_("bairro"), max_length=72)
    
    # payment
    payment_type = models.ForeignKey("PaymentType", verbose_name=_("payment type"), on_delete=models.RESTRICT)
    payment_type_name = models.CharField(_("payment type"), max_length=30)
    change_to = models.PositiveSmallIntegerField(_("change to"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    shipping_fee = models.ForeignKey("ShippingFee", verbose_name=_("shipping fee"), on_delete=models.RESTRICT, null=True)
    shipping_fee_value = models.PositiveSmallIntegerField(_("shipping fee value"), null=True, validators=[MaxValueValidator(32767)])
    total = models.PositiveIntegerField(verbose_name=_("total"), validators=[MaxValueValidator(2147483647)])
    
    # infos
    status = models.ForeignKey("Status", verbose_name=_("status"), on_delete=models.RESTRICT, default=1)
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
        
    def setUser(self, user: User):
        self.user_request = user
        self.full_name = user.get_full_name()
        self.phone = user.phone
        self.email = user.email
        
    def setAddress(self, add: Address):
        self.address = add
        self.address_number = add.number
        self.address_complement = add.complement
        self.logradouro_cep = add.logradouro.cep
        self.logradouro_name = add.logradouro.fullname()
        self.uf_acronym = add.logradouro.uf.acronym
        self.bairro_name = add.logradouro.bairro.name
    
    def setClient(self, client: Client):
        self.client = client
        self.full_name = client.full_name
        self.phone = client.phone
        self.address_number = client.number
        self.address_complement = client.complement
        self.logradouro_cep = client.logradouro.cep
        self.logradouro_name = client.logradouro.fullname()
        self.uf_acronym = client.logradouro.uf.acronym
        self.bairro_name = client.logradouro.bairro.name
    
    def fphone(self):
        if self.phone != None:
            return f"({self.phone[0:2]}) {self.phone[2:7]}-{self.phone[7:]}"
        else:
            return self.phone
        
    def ftotal(self):
        total = 0
        if getattr(self, "total", 0) > 0:
            total = self.total
        return locale.currency(total / 100, grouping=True)
    
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
    quantity = models.PositiveSmallIntegerField(verbose_name=_("quantity"), default=1, validators=[MaxValueValidator(32767)])
    total = models.PositiveIntegerField(verbose_name=_("total"), default=1, validators=[MaxValueValidator(2147483647)])
    
    option1 = models.CharField(verbose_name=_("option name"), null=True, blank=True, max_length=15)
    price1 = models.PositiveSmallIntegerField(verbose_name=_("option price"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    option2 = models.CharField(verbose_name=_("option name"), null=True, blank=True, max_length=15)
    price2 = models.PositiveSmallIntegerField(verbose_name=_("option price"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    option3 = models.CharField(verbose_name=_("option name"), null=True, blank=True, max_length=15)
    price3 = models.PositiveSmallIntegerField(verbose_name=_("option price"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    option4 = models.CharField(verbose_name=_("option name"), null=True, blank=True, max_length=15)
    price4 = models.PositiveSmallIntegerField(verbose_name=_("option price"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    option5 = models.CharField(verbose_name=_("option name"), null=True, blank=True, max_length=15)
    price5 = models.PositiveSmallIntegerField(verbose_name=_("option price"), null=True, blank=True, validators=[MaxValueValidator(32767)])
    
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
        self.sef_total()
            
        super().save(*args, **kwargs)

    
    def percentage_discount(self):
        percentage = None
        if self.discount:
            percentage = int(float(self.discount) * 100)
        return percentage
    
    def fpercentage_discount(self):
        percentage = None
        if self.percentage_discount():
            percentage = f"{self.percentage_discount()}%"
        return percentage
    
    def fprice(self):
        price = None
        if self.price:
            price = locale.currency(self.price / 100, grouping=True)
        return price
    
    def total_options(self):
        total = 0
        for index in range(5):
            field = f"price{index}"
            if hasattr(self, field):
                price = getattr(self, field) or 0
                total = total + price
        return total
    
    def ftotal(self):
        total = 0
        if getattr(self, "total", 0) > 0:
            total = self.total
        return locale.currency(total / 100, grouping=True)
    
    def fquantity(self):
        units = f"{self.quantity} unidades"
        unit = f"{self.quantity} unidade"
        return units if self.quantity > 1 else unit
    
    
    def sef_total(self):
        discount = self.discount if self.discount else 0
        quantity = self.quantity if self.quantity else 0
        total_options = self.total_options()
        price = (self.price if self.price else 0) + total_options
        
        disc = float(discount * quantity) * price
        total = (price * quantity) - disc
        
        self.total = round(total)
    
    def set_options(self, options: QuerySet[Option]):
        for index, option in enumerate(options):
            setattr(self, f"option{index + 1}", option.name)
            setattr(self, f"price{index + 1}", option.price)
    
    def foptions(self):
        options = []
        
        for index in range(5):
            name = getattr(self, f"option{index + 1}")
            price = getattr(self, f"price{index + 1}")
            
            if price:
                price = locale.currency(price / 100, grouping=True)
            
            if name and price:
                options.append({ "name": name, "fprice": price })
            
        return options
    
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
