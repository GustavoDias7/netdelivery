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
        

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
    
class FirstNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]
        
class LastNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name"]
    
class PhoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone"]
    
class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
    
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