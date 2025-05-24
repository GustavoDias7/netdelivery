from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ShippingFee, Order
        
class ShippingFeeForm(forms.ModelForm):
    value = forms.CharField(
        widget=forms.TextInput(
            attrs={'data-mask': 'currency'}
        )
    )
    
    class Meta:
        model = ShippingFee
        fields = "__all__"
        widgets = {'user': forms.HiddenInput()}
        
    class Media:
        js = ('js/pages/admin_shipping_fee.js',)
        
class OrderForm(forms.ModelForm):
    change_to = forms.CharField(
        widget=forms.TextInput(
            attrs={'data-mask': 'currency'}
        )
    )
    
    class Meta:
        model = Order
        fields = "__all__"
        
    class Media:
        js = ('js/pages/admin_order.js',)
