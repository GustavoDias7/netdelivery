from django.db import models
from django.db.models.functions import Now
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from .validators import (cep_validator, name_validator, phone_validator)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import locale 
import re
from product.models import (ProductVariant, Combo)
from address.models import (Logradouro, WhiteListBairro)

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

class Order(models.Model):
    client = models.ForeignKey("Client", null=True, on_delete=models.SET_NULL)
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
    product = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.RESTRICT)
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
        percentage = int(float(self.product_discount) * 100)
        return percentage
    
    def fpercentage_discount(self):
        return f"{self.percentage_discount()}%"
    
    def ftotal_price(self):
        disc = float(self.product_discount * self.quantity) * self.product_price
        fee = self.order.shipping_fee_value if self.order.shipping_fee_value != None else 0
        total = ((self.product_price * self.quantity) - disc) + fee
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
    value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(32767)])
    whitelistbairro = models.OneToOneField(WhiteListBairro, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(_('Default'), default=False)
    
    class Meta:
        verbose_name = _("Shipping fee")
        verbose_name_plural = _("Shipping fees")
        
    def fvalue(self):
        float_value = self.value / 100
        formatted_value = locale.currency(float_value, grouping=True)
        return formatted_value
    
    def __str__(self):
        if self.whitelistbairro:
            return f"{self.id}: {self.whitelistbairro.bairro.name}"
        elif self.is_default:
            return f"{self.id}: {_('default')}"
        else:
            return f"{self.id}"

class OrderAddress(models.Model):
    address_number = models.PositiveSmallIntegerField(_("Number"), blank=True, null=True, validators=[MaxValueValidator(32767)]) 
    address_complement = models.CharField(_("Complement"), max_length=100, blank=True, null=True)
    uf_acronym = models.CharField("UF", max_length=2, validators=[MinLengthValidator(2)])
    logradouro_cep = models.CharField("CEP", max_length=8, validators=[cep_validator])
    logradouro_name = models.CharField("Nome do logradouro", max_length=100)
    logradouro_type = models.CharField("Tipo do logradouro", max_length=36)
    localidade_name = models.CharField("Localidade", max_length=72)
    bairro_name = models.CharField("Bairro", max_length=72)
    
    def set(self, addr):
        self.address_number = addr.number
        self.address_complement = addr.complement
        self.uf_acronym = addr.logradouro.uf.acronym
        self.logradouro_cep = addr.logradouro.cep
        self.logradouro_name = addr.logradouro.name
        self.logradouro_type = addr.logradouro.type
        self.localidade_name = addr.logradouro.localidade.name
        self.bairro_name = addr.logradouro.bairro.name
    
    def __str__(self):
        return f"{self.logradouro_type} {self.logradouro_name}, {self.localidade_name} - {self.uf_acronym}"

class UserManager(BaseUserManager):
    def _create_user(
        self, username, email, password, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()
        if not username:
            raise ValueError(_("The given username must be set"))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters"
        ),
        validators=[
            validators.RegexValidator(
                re.compile("^[a-zA-Z0-9_.-]+$"), _("Enter a valid username."), _("invalid")
            )
        ],
    )

    first_name = models.CharField(_("first name"), max_length=30, validators=[name_validator])

    last_name = models.CharField(_("last name"), max_length=30, validators=[name_validator])

    email = models.EmailField(_("email address"), max_length=255, unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_trusty = models.BooleanField(
        _("trusty"),
        default=False,
        help_text=_("Designates whether this user has confirmed his account."),
    )
    
    phone = models.CharField(max_length=11, null=True, validators=[phone_validator])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def fphone(self):
        if self.phone != None:
            return f"({self.phone[0:2]}) {self.phone[2:7]}-{self.phone[7:]}"
        else:
            return self.phone
    
    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def get(self, name):
        return getattr(self, name)
    
    def set(self, name, value):
        print(self, name, value)
        setattr(self, name, value)

    # def email_user(self, subject, message, from_email=None):
    #     send_mail(subject, message, from_email, [self.email])
    
class Client(models.Model):
    full_name = models.CharField(_("Full name"), max_length=60)
    logradouro = models.ForeignKey(Logradouro, null=True, on_delete=models.SET_NULL, help_text="Pesquise pelo CEP, nome do logradouro, nome da localidade ou nome do bairro.")
    number = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(32767)]) 
    complement = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(_("Number Phone"), max_length=11, null=True, blank=True, validators=[phone_validator])
    cpf = models.CharField("CPF", max_length=11, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.full_name:
            self.full_name = self.full_name.upper()
        super(Client, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} {self.cpf if self.cpf else ''}"
    
