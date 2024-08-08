from django import forms
from .models import User, Address

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
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
    
class CepForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["cep"]
        
class NumberForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["number"]
        
class ComplementForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["complement"]