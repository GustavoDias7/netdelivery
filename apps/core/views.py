from django.shortcuts import render
from apps.product.models import (
    Combo,
    ProductVariant,
)
from django.core.exceptions import ObjectDoesNotExist

def homepage(request):
    context = {
        "categories": {},
        "combos": []
    }
        
    try:
        queryset_variants = ProductVariant.objects.filter(archived=False, default=True)
        categories = {}
        for variant in queryset_variants:
            category = variant.product.category.name
            if categories.get(category) == None:
                categories[category] = []
            categories[category].append(variant)
        context["categories"] = categories
    except ObjectDoesNotExist:
        categories = None
    
    try:
        queryset_combos = Combo.objects.filter(archived=False)
        combos = []
        for combo in queryset_combos:
            combos.append(combo)
        context["combos"] = combos
    except ObjectDoesNotExist:
        combos = None
        
    
    return render(request, "pages/homepage.html", context)

