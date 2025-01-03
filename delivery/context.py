from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from apps.user.models import (
    Contacts, 
    OpeningHours,
    User
)
from apps.product.models import (
    Combo,
    ProductVariant,
    Category
)

def header(request):
    if request.resolver_match == None: 
        return {}
    else:
        if 'username' in request.resolver_match.kwargs:
            username = request.resolver_match.kwargs.get("username")
        else:
            return {}
    
    context = {
        "header_categories": [],
        "header_combos": False,
        "logo": ""
    }
    
    try:
        owner = User.objects.get(username=username, is_owner=True)
        context["logo"] = owner.get_full_name()
    except ObjectDoesNotExist:
        pass
    
    categories_cache = cache.get(f"{username}_header_categories")
    if categories_cache == None:
        try:
            qs_categories = Category.objects.all()
            for category in qs_categories:
                variant = ProductVariant.objects.filter(archived=False, product__category=category, product__user__username=username).first()
                if variant:
                    context["header_categories"].append(variant.product.category)
            cache.set(f"{username}_header_categories", context["header_categories"])
        except ObjectDoesNotExist:
            context["header_categories"] = None
    else:
        context["header_categories"] = categories_cache
    
    combos_cache = cache.get(f"{username}_header_combos")
    if combos_cache == None:
        try:
            qs_combos = Combo.objects.filter(archived=False, user__username=username).first()
            if qs_combos:
                context["header_combos"] = True
                cache.set(f"{username}_header_combos", context["header_combos"])
        except ObjectDoesNotExist:
            context["header_combos"] = None
    else:
        context["header_combos"] = combos_cache
    
    return context

def contacts(request):
    if request.resolver_match == None: 
        return {}
    else:
        if 'username' in request.resolver_match.kwargs:
            username = request.resolver_match.kwargs.get("username")
        else:
            return {}
    
    context = {
        "contacts": None,
        "opening_hours": None
    }
    
    contacts_cache = cache.get(f"{username}_contacts")
    if contacts_cache == None:
        try:
            qs_contacts = Contacts.objects.filter(user__username=username).first()
            context["contacts"] = qs_contacts
            cache.set(f"{username}_contacts", context["contacts"])
        except ObjectDoesNotExist:
            context["contacts"] = None
    else:
        context["contacts"] = contacts_cache
        
    opening_hours_cache = cache.get(f"{username}_opening_hours")
    if opening_hours_cache == None:
        try:
            qs_opening_hours = OpeningHours.objects.filter(contacts=qs_contacts)
            context["opening_hours"] = qs_opening_hours
            cache.set(f"{username}_opening_hours", context["opening_hours"])
        except ObjectDoesNotExist:
            context["opening_hours"] = None
    else:
        context["opening_hours"] = opening_hours_cache
        
    
    return context