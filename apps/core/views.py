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
    
    categories_cache = cache.get(f"{username}_categories")
    if categories_cache == None:
        try:
            queryset_variants = ProductVariant.objects.filter(archived=False, default=True, product__user__username=username)
            
            categories = {}
            for variant in queryset_variants:
                category = variant.product.category.name
                if categories.get(category) == None:
                    categories[category] = []
                categories[category].append(variant)
            context["categories"] = categories
            cache.set(f"{username}_categories", context["categories"])
        except ObjectDoesNotExist:
            categories = None
    else:
        context["categories"] = categories_cache
    
    combos_cache = cache.get(f"{username}_combos")
    if combos_cache == None:
        try:
            queryset_combos = Combo.objects.filter(archived=False, user__username=username)
            combos = []
            for combo in queryset_combos:
                combos.append(combo)
            context["combos"] = combos
            cache.set(f"{username}_combos", context["combos"])
        except ObjectDoesNotExist:
            combos = None
    else:
        context["combos"] = combos_cache
    
    return render(request, "pages/homepage.html", context)

def permission_denied(request, exception):
    return render(request, 'pages/403.html', status=403)

def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)

def server_error(request):
    return render(request, 'pages/500.html', status=500)