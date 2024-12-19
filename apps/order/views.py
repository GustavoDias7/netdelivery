from django.shortcuts import render, redirect
from .models import (
    Order,
    OrderItem,
    ShippingFee,
    PaymentType,
    OrderStatus
)
from apps.product.models import ProductVariant
from apps.address.models import (Address, WhiteList, Bairro)
from apps.user.models import User
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
import json
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from apps.core.validators import cart_validator
from delivery.utils import remove_non_numeric
from django.core.exceptions import ObjectDoesNotExist

def orders(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    order = Order.objects.filter(user_owner__username=username, user_request=request.user).order_by('-created')
    page_size = 10
    paginated_order = Paginator(order, page_size).page(1)
    
    if request.method == 'POST':
        order_id = request.POST.get('cancel_order')
        cancel_order = order.get(pk=order_id)
        order_status = OrderStatus.objects.get(code="canceled")
        if cancel_order.order_status.code == 'wating':
            cancel_order.order_status = order_status
            cancel_order.save()
    
    order_items = OrderItem.objects \
        .select_related('order') \
        .filter(order__in=paginated_order, order__user_request=request.user) \
        .order_by('-order__created')
    
    context["orders"] = {}
    for item in order_items:
        if item.order.id in context["orders"]:
            context["orders"][item.order.id].append(item)
        else:
            context["orders"][item.order.id] = []
            context["orders"][item.order.id].append(item)
    
        
    return render(request, 'pages/orders.html', context)

def order(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    context["field"] = {}
    
    try:
        address = Address.objects.get(user=request.user)
        context["address"] = address
        
        whitelist = WhiteList.objects.get(user__username=username)
        wl_bairro = whitelist.bairros.get(id=address.logradouro.bairro.id)
        shippingfee = ShippingFee.objects.get(user__username=username, bairro=wl_bairro)
        context["shippingfee"] = shippingfee
    except WhiteList.DoesNotExist:
        whitelist = None
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
        change_to = request.POST.get("change_to")
        
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
        
        product_variants = ProductVariant.objects.filter(filter_list, product__user__username=username)
        
        for item in cart:
            try:
                product_id = item.get('id')
                variant = product_variants.get(pk=product_id)
                if variant.price != item.get("price"):
                    raise ValidationError(
                        _(f"O preço do produto {variant.full_name()} é de {variant.fprice()}.")
                    )
                if variant.stock != None:
                    if variant.stock == 0:
                        raise ValidationError(
                            _(f'"{variant.full_name()}" está sem estoque.')
                        )
                    if variant.stock < item.get("count"):
                        raise ValidationError(
                            _(f"{variant.full_name()} tem {variant.stock} unidades em estoque.")
                        )
                        
            except ValidationError as e:
                context["notification"] = e.message
                return render(request, "pages/order.html", context)
            except ObjectDoesNotExist:
                context["notification"] = f'O produto com id: "{product_id}" não existe.'
                return render(request, "pages/order.html", context)
        
        order = Order()
        order.user_request = request.user
        
        try:
            order.user_owner = User.objects.get(username=username)
        except User.DoesNotExist:
            context["notification"] = f"A conta '{username}' não existe."
            return render(request, "pages/order.html", context)
        
        try:
            payment_type = PaymentType.objects.get(code=payment_code)
            order.setPaymentType(payment_type)
            if change_to != None:
                change_int = int(remove_non_numeric(change_to))
                if change_int > 0:
                    order.change_to = change_int
        except PaymentType.DoesNotExist:
            context["notification"] = "Selecione uma forma de pagamento."
            return render(request, "pages/order.html", context)
        
        if is_delivery and shippingfee:
            order.setShippingFee(shippingfee)
        
        order.save()
        
        for item in cart:
            variant = product_variants.get(pk=item.get("id"))
            order_item = OrderItem()
            
            order_item.order=order
            order_item.product=variant
            order_item.price=variant.price
            order_item.discount=variant.discount
            order_item.quantity=item.get("count")
            
            if variant.stock != None:
                variant.stock -= order_item.quantity 
            
            order_item.save()
            variant.save()
        
        response = redirect('success', username)
        response.set_cookie('reset_cart', True, max_age=99999, secure=True, httponly=True)
        return response
        
    return render(request, "pages/order.html", context)


def success(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    
    reset_cart = request.COOKIES.get('reset_cart')
    if reset_cart:
        context["reset_cart"] = True
        response = render(request, 'pages/success.html', context)
        response.delete_cookie("reset_cart")
        return response

    return render(request, 'pages/success.html', context)