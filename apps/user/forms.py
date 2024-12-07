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
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={ 'data-mask': 'cellphone' })
    )
    phone_number = forms.CharField(
        label=_("Phone number"),
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={ 'data-mask': 'phone' })
    )
    whatsapp_message = forms.CharField(
        label=_("WhatsApp message"),
        required=False,
        max_length=100,
        widget=forms.Textarea(attrs={ 'rows': '3' })
    )
    class Meta:
        model = Contacts
        fields = "__all__"
        widgets = {'user': forms.HiddenInput()}
    
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
        
class OpeningHoursForm(forms.ModelForm):
    inital_hour = forms.TimeField(
        label=_("Initial hour"), 
        required=False, 
        widget=forms.TimeInput(format='%H:%M', attrs={ 'data-mask': 'time' })
    )
    final_hour = forms.TimeField(
        label=_("Final hour"), 
        required=False, 
        widget=forms.TimeInput(format='%H:%M', attrs={ 'data-mask': 'time' })
    )
    def clean(self):
        data = self.cleaned_data
        
        final_day = data.get('final_day', None)
        inital_hour = data.get('inital_hour', None)
        final_hour = data.get('final_hour', None)
        closed = data.get('closed', None)
        
        fields = [final_day, inital_hour, final_hour]
        
        if closed == False and None in fields:
            if final_day == None: self.add_error("final_day", _('This field is required.'))
            if inital_hour == None: self.add_error("inital_hour", _('This field is required.'))
            if final_hour == None: self.add_error("final_hour", _('This field is required.'))
        