from django.shortcuts import render
from apps.product.models import (Combo, ProductVariant)
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

def homepage(request):
    context = {
        "categories": {},
        "combos": []
    }
    
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

