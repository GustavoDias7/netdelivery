from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from apps.core.validators import (name_validator, phone_validator, cellphone_number)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import re
from apps.address.models import Logradouro
from apps.core.utils import remove_non_numeric

class Contacts(models.Model):
    whatsapp_number = models.CharField(_("WhatsApp number"), max_length=11, validators=[cellphone_number])
    whatsapp_message = models.URLField(_("WhatsApp message"), max_length=100)
    facebook_link = models.URLField(_("Facebook link"))
    instagram_link = models.URLField(_("Instagram link"))
    linkedin_link = models.URLField(_("LinkedIn link"))
    x_link = models.URLField(_("X link"))
    phone_number = models.CharField(_("Telephone number"), max_length=11, validators=[phone_validator])
    email = models.EmailField(_("E-mail"), max_length=255)
    address_text = models.CharField(_("Address text"), max_length=30)
    address_link = models.URLField(_("Address link"))
    
    def clean_fields(self, exclude=None):
        self.whatsapp_number = remove_non_numeric(self.whatsapp_number)
        self.phone_number = remove_non_numeric(self.phone_number)
        super().clean_fields(exclude=exclude)
    
    def fphone_number(self):
        if not self.phone_number:
            ddd = self.phone[0:2]
            
            if len(self.phone_number) == 11:
                part1 = self.phone[2:7]
                part2 = self.phone[7:]
            else:
                part1 = self.phone[2:6]
                part2 = self.phone[6:]
            
            return f"({ddd}) {part1}-{part2}"
        else:
            return self.phone_number
    
    def fwhatsapp_number(self):
        if not self.whatsapp_number:
            ddd = self.phone[0:2]
            part1 = self.phone[2:7]
            part2 = self.phone[7:]
            return f"({ddd}) {part1}-{part2}"
        else:
            return self.whatsapp_number
    
    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")
        
    def __str__(self):
        return f"Contacts id {self.id}"

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
    
