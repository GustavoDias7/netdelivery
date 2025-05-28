from django.shortcuts import render
from .models import ProductVariant, Combo, ComboItem, Option, OptionGroup

def product(request, username):
    variant_id = request.GET.get('variant', "")
    product_id = request.GET.get('id', "")
    variants = ProductVariant.objects.filter(product_id=product_id, product__user__username=username)
    variant = variants.get(id=variant_id)
    option_group = None
    options = None
    try:
        option_group = OptionGroup.objects.get(product_variant=variant)
        options = Option.objects.filter(option_group=option_group)
    except:
        pass
    
    context = {
        "variants": variants,
        "variant": variant,
        "options": options,
        "option_group": option_group,
        "username": username
    }
    
    return render(request, "pages/product.html", context)

def combo(request, username):
    combo_id = request.GET.get('id', "")
    combo = Combo.objects.get(id=combo_id, user__username=username)
    items = ComboItem.objects.filter(combo__id=combo_id, product_variant__archived=False)
    context = { "combo": combo, "items": items, "username": username }
    
    return render(request, "pages/combo.html", context)