from django import forms
from django.utils.translation import gettext_lazy as _
from apps.order import models
from django.utils.safestring import mark_safe
import locale 


class ShippingFeeForm(forms.ModelForm):
    value = forms.CharField(
        widget=forms.TextInput(
            attrs={'data-mask': 'currency'}
        )
    )
    
    class Meta:
        model = models.ShippingFee
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
        model = models.Order
        fields = "__all__"
        
        
class ReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f"<div class='readonly'>{value}</div>")
class CurrencyReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        price = None
        if value:
            price = locale.currency(int(value) / 100, grouping=True)
            
        return mark_safe(f"<div class='readonly'>{price}</div>")

class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        options_to_hide_if_none = [
            "option1",
            "option2",
            "option3",
            "option4",
            "option5",
        ]
        prices_to_hide_if_none = [
            "price1",
            "price2",
            "price3",
            "price4",
            "price5",
        ]
        if instance and instance.pk:
            for field in options_to_hide_if_none:
                if getattr(instance, field, None) != None:
                    self.fields[field].widget = ReadOnlyWidget()
                    self.fields[field].disabled = True
                else:
                    self.fields[field].widget = forms.HiddenInput()
                    
            for field in prices_to_hide_if_none:
                if getattr(instance, field, None) != None:
                    self.fields[field].widget = CurrencyReadOnlyWidget()
                    self.fields[field].disabled = True
                else:
                    self.fields[field].widget = forms.HiddenInput()