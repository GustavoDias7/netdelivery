from django import forms
from .models import User, Contacts

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
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'v-model': 'fields.whatsapp_number',
                'v-mask':"'(##) #####-####'", 
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'v-model': 'fields.phone_number',
                'v-mask':"['(##) ####-####', '(##) #####-####']", 
            }
        )
    )
    class Meta:
        model = Contacts
        fields = "__all__"