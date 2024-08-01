from django import forms
from .models import User
from django.core import validators
import re
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
class FirstNameForm(forms.Form):
    first_name = forms.CharField(max_length=30)
        
class LastNameForm(forms.Form):
    last_name = forms.CharField(max_length=30)
    
class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11)
    
class UsernameForm(forms.Form):
    phone = forms.CharField(max_length=15, validators=[
        validators.RegexValidator(
            re.compile("^[a-zA-Z0-9_.-]+$"), _("Enter a valid username."), _("invalid")
        )
    ],)
    
class CepForm(forms.Form):
    cep = forms.CharField(max_length=8, validators=[validators.MinLengthValidator(8)])
class DistrictForm(forms.Form):
    pass
class AddressForm(forms.Form):
    pass
class NumberForm(forms.Form):
    pass
class ComplementForm(forms.Form):
    pass