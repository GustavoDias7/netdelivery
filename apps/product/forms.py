from django import forms
from .models import (Product, ProductVariant, Combo, Option)
from django.utils.translation import gettext_lazy as _

class OptionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('name')}
        )
    )
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'data-mask': 'currency', 
                'placeholder': _('price'), 
            }
        )
    )
    class Meta:
        model = Option
        fields = "__all__"
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {'user': forms.HiddenInput()}

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
        widgets = {'user': forms.HiddenInput()}
        
    class Media:
        js = ('js/pages/admin_combos.js',)