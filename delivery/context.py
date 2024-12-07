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
    usarname = request.resolver_match.kwargs["username"]
    
    context = {
        "header_categories": [],
        "header_combos": False
    }
    
    categories_cache = cache.get(f"{usarname}_header_categories")
    if categories_cache == None:
        try:
            qs_categories = Category.objects.all()
            for category in qs_categories:
                variant = ProductVariant.objects.filter(archived=False, product__category=category).first()
                if variant:
                    context["header_categories"].append(variant.product.category)
            cache.set(f"{usarname}_header_categories", context["header_categories"])
        except ObjectDoesNotExist:
            context["header_categories"] = None
    else:
        context["header_categories"] = categories_cache
    
    combos_cache = cache.get(f"{usarname}_header_combos")
    if combos_cache == None:
        try:
            qs_combos = Combo.objects.filter(archived=False).first()
            if qs_combos:
                context["header_combos"] = True
                cache.set(f"{usarname}_header_combos", context["header_combos"])
        except ObjectDoesNotExist:
            context["header_combos"] = None
    else:
        context["header_combos"] = combos_cache
    
    return context

def contacts(request):
    usarname = request.resolver_match.kwargs["username"]
    context = {
        "contacts": None,
        "opening_hours": None
    }
    
    contacts_cache = cache.get(f"{usarname}_contacts")
    if contacts_cache == None:
        try:
            qs_contacts = Contacts.objects.filter(user__username=usarname).first()
            context["contacts"] = qs_contacts
            cache.set(f"{usarname}_contacts", context["contacts"])
        except ObjectDoesNotExist:
            context["contacts"] = None
    else:
        context["contacts"] = contacts_cache
        
    opening_hours_cache = cache.get(f"{usarname}_opening_hours")
    if opening_hours_cache == None:
        try:
            qs_opening_hours = OpeningHours.objects.filter(contacts=qs_contacts)
            context["opening_hours"] = qs_opening_hours
            cache.set(f"{usarname}_opening_hours", context["opening_hours"])
        except ObjectDoesNotExist:
            context["opening_hours"] = None
    else:
        context["opening_hours"] = opening_hours_cache
        
    
    return context