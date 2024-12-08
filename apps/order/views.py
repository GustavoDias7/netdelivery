from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import (
    Order,
    OrderItem,
    ShippingFee,
    PaymentType,
    OrderItemStatus
)
from apps.product.models import Product
from apps.address.models import (Address, WhiteList, Bairro)
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
import json
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from apps.core.validators import cart_validator
from django.core.exceptions import ObjectDoesNotExist

@login_required
def orders(request, username):
    context = {"username": username}
    order = OrderItem.objects.all().order_by('-id')
    page_size = 10
    paginated_order = Paginator(order, page_size).page(1)
    context["orders"] = paginated_order
    
    if request.method == 'POST':
        order_id = request.POST.get('cancel_order')
        order_item = order.get(pk=order_id)
        order_status = OrderItemStatus.objects.get(code="canceled")
        if order_item.order_item_status.code == 'wating':
            order_item.order_item_status = order_status
            order_item.save()
        
    return render(request, 'pages/orders.html', context)

@login_required
def order(request, username):
    context = {"username": username}
    context["field"] = {}
    
    try:
        address = Address.objects.get(user=request.user)
        context["address"] = address
        
        whitelist = WhiteList.objects.get(user__username=username)
        wl_bairro = whitelist.bairros.get(id=address.logradouro.bairro.id)
        shippingfee = ShippingFee.objects.get(user__username=username, bairro=wl_bairro)
        context["shippingfee"] = shippingfee
    except Bairro.DoesNotExist:
        context["field"].update({"address": {"errors": "Não operamos neste endereço."}})
    except Address.DoesNotExist:
        address = None
        shippingfee = None
    except ShippingFee.DoesNotExist:
        try:
            shippingfee = ShippingFee.objects.get(user__username=username, is_default=True)
            context["shippingfee"] = shippingfee
        except ShippingFee.DoesNotExist:
            shippingfee = None
        
    if request.method == "POST":
        cart = json.loads(request.POST.get("cart")) 
        is_delivery = request.POST.get("is_delivery", False) == 'true'
        payment_code = request.POST.get("payment_type")
        
        if len(cart) == 0:
            context["notification"] = "Adicione itens ao carrinho."
            return render(request, "pages/order.html", context)
        
        try:
            cart_validator(cart)
        except ValidationError as e:
            context["notification"] = e.message
            return render(request, "pages/order.html", context)
        
        if is_delivery and address == None:
            context["notification"] = "Adicione seu endereço."
            return render(request, "pages/order.html", context)
            
        filter_list = Q()
        for item in cart:
            filter_list |= Q(pk=item.get("id"))
        
        products = Product.objects.filter(filter_list)
        
        for item in cart:
            try:
                product_id = item.get('id')
                product = products.get(pk=product_id)
                if product.price != item.get("price"):
                    raise ValidationError(
                        _(f"O preço do produto {product.name} é de {product.fprice()}.")
                    )
                if product.stock == 0:
                    raise ValidationError(
                        _(f'"{product.name}" está sem estoque.')
                    )
                if product.stock < item.get("count"):
                    raise ValidationError(
                        _(f"{product.name} tem {product.stock} unidades em estoque.")
                    )
            except ValidationError as e:
                context["notification"] = e.message
                return render(request, "pages/order.html", context)
            except ObjectDoesNotExist:
                context["notification"] = f'O produto com id: "{product_id}" não existe.'
                return render(request, "pages/order.html", context)
        
        order = Order()
        order.user = request.user
        
        try:
            payment_type = PaymentType.objects.get(code=payment_code)
            order.setPaymentType(payment_type)
        except PaymentType.DoesNotExist:
            context = {"notification": "Selecione uma forma de pagamento."}
            return render(request, "pages/order.html", context)
        
        if is_delivery and shippingfee:
            order.setShippingFee(shippingfee)
            
            # try:
            #     if address.order_address:
            #         order.order_address = address.order_address
            #     else:
            #         raise ObjectDoesNotExist()
            # except ObjectDoesNotExist:
            #     order_address = OrderAddress()
            #     order_address.set(address)
            #     order_address.save()
                
            #     order.order_address = order_address
                
            #     address.order_address = order_address
            #     address.save()
        
        order.save()
        
        for item in cart:
            product = products.get(pk=item.get("id"))
            order_item = OrderItem(
                order=order,
                product=product,
                product_price=product.price,
                product_discount=product.discount,
                quantity=item.get("count"),
            )
            product.stock -= order_item.quantity 
            
            order_item.save()
            product.save()
        
    return render(request, "pages/order.html", context)