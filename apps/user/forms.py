from django import forms
from .models import User, Contacts, Client
from django.utils.translation import gettext_lazy as _

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
        
class ContactsForm(forms.ModelForm):
    whatsapp_number = forms.CharField(
        label=_("WhatsApp number"),
        max_length=15,
        widget=forms.TextInput(attrs={ 'data-mask': 'cellphone' })
    )
    phone_number = forms.CharField(
        label=_("Phone number"),
        max_length=15,
        widget=forms.TextInput(attrs={ 'data-mask': 'phone' })
    )
    class Meta:
        model = Contacts
        fields = "__all__"
    
    class Media:
        js = ('js/pages/admin_contacts.js',)
        
class ClientsForm(forms.ModelForm):
    phone = forms.CharField(
        label=_("Phone Number"),
        max_length=15,
        widget=forms.TextInput(attrs={ 'data-mask': 'phone' })
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs={ 'data-mask': 'cpf' })
    )
    class Meta:
        model = Client
        fields = "__all__"
    
    class Media:
        js = ('js/pages/admin_client.js',)