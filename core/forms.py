from django import forms
from core.validators import cep_validator
    
class CepForm(forms.Form):
    cep = forms.CharField(max_length=8, validators=[cep_validator])
        
class NumberForm(forms.ModelForm):
    class Meta:
        # model = Address
        fields = ["number"]
        
class ComplementForm(forms.ModelForm):
    class Meta:
        # model = Address
        fields = ["complement"]
       