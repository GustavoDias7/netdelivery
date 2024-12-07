from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ShippingFee
        
class ShippingFeeForm(forms.ModelForm):
    class Meta:
        model = ShippingFee
        fields = "__all__"
        widgets = {'user': forms.HiddenInput()}
