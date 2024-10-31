from django import forms
from .models import (ProductVariant, Combo)

class ProductVariantForm(forms.ModelForm):
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={'data-mask': 'currency'}
        )
    )
    class Meta:
        model = ProductVariant
        fields = "__all__"
        
    class Media:
        js = ('js/pages/admin_product.js',)
        
class ComboForm(forms.ModelForm):
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={'data-mask': 'currency'}
        )
    )
    class Meta:
        model = Combo
        fields = "__all__"
        
    class Media:
        js = ('js/pages/admin_combos.js',)