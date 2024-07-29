from django.db import models
from django.db.models.functions import Now
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator)
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import re

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()
    # image = models.ImageField()
    description = models.TextField(max_length=400)
    stock = models.PositiveIntegerField()
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
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    payment_type = models.ForeignKey("PaymentType", on_delete=models.RESTRICT)
    shipping_tax = models.ForeignKey("ShippingTax", on_delete=models.RESTRICT, null=True)
    shipping_tax_name = models.CharField(max_length=50, null=True)
    shipping_tax_value = models.PositiveSmallIntegerField(null=True)
    created = models.DateTimeField(db_default=Now())
    
    def __str__(self):
        return f"Order: {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.RESTRICT)
    order_status = models.ForeignKey("OrderStatus", on_delete=models.RESTRICT, default=1)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    product_price = models.PositiveSmallIntegerField()
    product_discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"Order item: {self.id}"
    
class OrderStatus(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name}"

class PaymentType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.name}"

class ShippingTax(models.Model):
    name = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.name}"
    
class Address(models.Model):
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    cep = models.CharField(max_length=8)
    district = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    number = models.PositiveSmallIntegerField(null=True)
    complement = models.CharField(max_length=50)
    
    def fcep(self):
        return f"{self.cep[0:5]}-{self.cep[5:]}"
    
    def __str__(self):
        return f"{self.fcep()}"

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

    first_name = models.CharField(_("first name"), max_length=30, validators=[MinLengthValidator(3)])

    last_name = models.CharField(_("last name"), max_length=30, validators=[MinLengthValidator(3)])

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
    
    phone = models.CharField(max_length=11, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def fphone(self):
        return f"({self.phone[0:2]}) {self.phone[2:7]}-{self.phone[7:]}"
    
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