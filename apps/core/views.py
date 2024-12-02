from django.shortcuts import render
from apps.product.models import (Combo, ProductVariant)
from apps.user.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

def homepage(request, username):
    context = {
        "categories": {},
        "combos": [],
        "username": username,
    }
    
    try:
        query_user = User.objects.get(username=username, is_superuser=False)
        print(query_user.__dict__)
    except ObjectDoesNotExist:
        print("This user do not exist!")
        
    
    categories_cache = cache.get("categories")
    if categories_cache == None:
        try:
            queryset_variants = ProductVariant.objects.filter(archived=False, default=True)
            categories = {}
            for variant in queryset_variants:
                category = variant.product.category.name
                if categories.get(category) == None:
                    categories[category] = []
                categories[category].append(variant)
            context["categories"] = categories
            cache.set("categories", context["categories"])
        except ObjectDoesNotExist:
            categories = None
    else:
        context["categories"] = categories_cache
    
    combos_cache = cache.get("combos")
    if combos_cache == None:
        try:
            queryset_combos = Combo.objects.filter(archived=False)
            combos = []
            for combo in queryset_combos:
                combos.append(combo)
            context["combos"] = combos
            cache.set("combos", context["combos"])
        except ObjectDoesNotExist:
            combos = None
    else:
        context["combos"] = combos_cache
    
    return render(request, "pages/homepage.html", context)

