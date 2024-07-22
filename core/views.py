from django.shortcuts import render
from core.models import (ProductCategory, Product)

def homepage(request):
    product_categories = ProductCategory.objects.values("id", "name")
    categories = []
    
    for category in product_categories:
        products = Product.objects.filter(product_category_id=category["id"])
        if len(products): categories.append(products)
    
    return render(request, "pages/homepage.html", {"categories": categories})

def order(request):
    return render(request, "pages/order.html")