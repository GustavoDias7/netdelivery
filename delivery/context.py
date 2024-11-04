from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
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
    
    categories_cache = cache.get("header_categories")
    
    if not categories_cache:
        try:
            qs_categories = Category.objects.all()
            for category in qs_categories:
                variant = ProductVariant.objects.filter(archived=False, product__category=category).first()
                if variant: context["header_categories"].append(variant.product.category)
                
            qs_combos = Combo.objects.filter(archived=False).first()
            if qs_combos: context["header_combos"] = True
            
            cache.set("header_categories", context)
        except ObjectDoesNotExist:
            context["qs_categories"] = None
            context["header_categories"] = None
    else:
        context = categories_cache
        
    return context

def contacts(request):
    context = {}
    
    contacts_cache = cache.get("contacts")
    if not contacts_cache:
        try:
            qs_contacts = Contacts.objects.filter().first()
            context["contacts"] = qs_contacts
        except ObjectDoesNotExist:
            context["contacts"] = None
        
        try:
            qs_opening_hours = OpeningHours.objects.filter(contacts=qs_contacts)
            context["opening_hours"] = qs_opening_hours
        except ObjectDoesNotExist:
            context["opening_hours"] = None
        
        cache.set("contacts", context)
    else:
        context = contacts_cache
    
    return context