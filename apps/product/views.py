from django.shortcuts import render
from .models import ProductVariant, Combo, ComboItem

def product(request, username):
    variant_id = request.GET.get('variant', "")
    product_id = request.GET.get('id', "")
    variants = ProductVariant.objects.filter(product_id=product_id, product__user__username=username)
    context = {
        "variants": variants.values("id", "product__id", "size_name", "short_size_name"),
        "variant": variants.get(id=variant_id),
        "username": username
    }
    
    return render(request, "pages/product.html", context)

def combo(request, username):
    combo_id = request.GET.get('id', "")
    combo = Combo.objects.get(id=combo_id, user__username=username)
    items = ComboItem.objects.filter(combo__id=combo_id, product_variant__archived=False)
    context = { "combo": combo, "items": items, "username": username }
    
    return render(request, "pages/combo.html", context)