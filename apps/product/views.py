from django.shortcuts import render
from .models import ProductVariant, Combo, ComboItem

def product(request):
    variant_id = request.GET.get('variant', "")
    product_id = request.GET.get('id', "")
    variants = ProductVariant.objects.filter(product_id=product_id)
    context = {
        "variants": variants.values("id", "product__id", "size_name", "short_size_name"),
        "variant": variants.get(id=variant_id),
    }
    
    return render(request, "pages/product.html", context)

def combo(request):
    combo_id = request.GET.get('id', "")
    combo = Combo.objects.get(id=combo_id)
    items = ComboItem.objects.filter(product_variant__archived=False)
    context = { "combo": combo, "items": items }
    
    return render(request, "pages/combo.html", context)