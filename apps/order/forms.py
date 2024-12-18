from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ShippingFee, Order
        
class ShippingFeeForm(forms.ModelForm):
    class Meta:
        model = ShippingFee
        fields = "__all__"
        widgets = {'user': forms.HiddenInput()}
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        
    class Media:
        js = ('js/pages/admin_order.js',)
