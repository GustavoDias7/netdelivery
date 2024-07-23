from django.shortcuts import render
from core.models import (ProductCategory, Product, Order, OrderItem, ShippingTax, PaymentType)
import json

def homepage(request):
    product_categories = ProductCategory.objects.values("id", "name")
    categories = []
    
    for category in product_categories:
        products = Product.objects.filter(product_category_id=category["id"])
        if len(products): categories.append(products)
    
    return render(request, "pages/homepage.html", {"categories": categories})

def order(request):
    context = {}
    if request.method == "POST":
        cart = json.loads(request.POST.get("cart")) # id, price, count(quantity), discount
        is_delivery = request.POST.get("is_delivery", False) == 'true'
        payment_code = request.POST.get("payment_type")
        
        order = Order()
        payment_type = PaymentType.objects.get(code=payment_code)
        order.payment_type = payment_type
        
        if is_delivery:
            # find tax by Address model
            shipping_tax = ShippingTax.objects.get(pk=1)
            order.shipping_tax = shipping_tax
            order.shipping_tax_name = shipping_tax.name
            order.shipping_tax_value = shipping_tax.value
        
        # validate all cart item with Product model
        
        
        order.save()
        
        for cart_item in cart:
            product = Product.objects.get(pk=cart_item.get("id"))
            order_item = OrderItem(
                order=order,
                product=product,
                product_price=product.price,
                product_discount=product.discount,
                quantity=cart_item.get("count"),
            )
            product.stock -= order_item.quantity 
            
            order_item.save()
            product.save()
        
    return render(request, "pages/order.html", context)