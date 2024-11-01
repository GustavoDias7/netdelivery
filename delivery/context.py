from apps.user.models import (
    Contacts, 
    OpeningHours
)
from apps.product.models import (
    Combo,
    ProductVariant,
    Category
)

def header_categories(request):
    context = {
        "header_categories": [],
        "header_combos": False
    }
    qs_categories = Category.objects.all()
    
    for category in qs_categories:
        variant = ProductVariant.objects.filter(archived=False, product__category=category).first()
        if variant: context["header_categories"].append(variant.product.category)
        
    qs_combos = Combo.objects.filter(archived=False).first()
    if qs_combos: context["header_combos"] = True
    
    return context

def contacts(request):
    context = {}
    
    qs_contacts = Contacts.objects.filter().first()
    qs_opening_hours = OpeningHours.objects.filter(contacts=qs_contacts)
    context["contacts"] = qs_contacts
    context["opening_hours"] = qs_opening_hours
    
    return context