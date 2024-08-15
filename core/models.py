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

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)])
    # image = models.ImageField()
    description = models.TextField(max_length=400, validators=[MinLengthValidator(4, _("Mínimo de 4 caracteres."))])
    stock = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(2147483647)])
    # stock == null/None == unlimited
    archived = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    product_category = models.ForeignKey("ProductCategory", on_delete=models.RESTRICT)
    
    def fprice(self):
        cents = int(self.price) / 100
        return f"{cents:.2f}".replace(".", ",")

    def __str__(self):
        return f"{self.name}"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    payment_type = models.ForeignKey("PaymentType", on_delete=models.RESTRICT)
    shipping_tax = models.ForeignKey("ShippingTax", on_delete=models.RESTRICT, null=True)
    shipping_tax_name = models.CharField(max_length=40, null=True)
    shipping_tax_value = models.PositiveSmallIntegerField(null=True, validators=[MaxValueValidator(32767)])
    created = models.DateTimeField(db_default=Now())
    received_date = models.DateTimeField(null=True)
    
    def fshipping_tax_value(self):
        float_value = self.shipping_tax_value / 100
        formatted_value = locale.currency(float_value, grouping=True)
        return formatted_value
    
    def __str__(self):
        return f"Order: {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.RESTRICT)
    order_item_status = models.ForeignKey("OrderItemStatus", on_delete=models.RESTRICT, default=1)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    product_price = models.PositiveIntegerField(validators=[MaxValueValidator(2147483647)])
    product_discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField(validators=[MaxValueValidator(32767)])
    
    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")
    
    def percentage_discount(self):
        percentage = int(float(self.product_discount) * 100)
        return percentage
    
    def fpercentage_discount(self):
        return f"{self.percentage_discount()}%"
    
    def ftotal_price(self):
        disc = float(self.product_discount * self.quantity) * self.product_price
        tax = self.order.shipping_tax_value if self.order.shipping_tax_value != None else 0
        total = ((self.product_price * self.quantity) - disc) + tax
        formatted_total = locale.currency(total / 100, grouping=True)
        return formatted_total
    
    def fquantity(self):
        units = f"{self.quantity} unidades"
        unit = f"{self.quantity} unidade"
        return units if self.quantity > 1 else unit
    
    def __str__(self):
        return f"Order item: {self.id}"
    
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

class ShippingTax(models.Model):
    name = models.CharField(max_length=40)
    value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(32767)])
    
    def __str__(self):
        return f"{self.name}"

class Address(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT, unique=True)
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
    
    # def __str__(self):
    #     return f"{self.fcep()}"

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
    
class Logradouro(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
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
        
    def __str__(self):
        return f"{self.type} {self.name}"
    
class UF(models.Model):
    acronym = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    
    def __str__(self):
        return f"{self.acronym}"

class Bairro(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=72)
    localidade = models.ForeignKey("Localidade", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"
    
class Localidade(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
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
    
