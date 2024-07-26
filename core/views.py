from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password
from core.models import (
    ProductCategory,
    Product,
    Order,
    OrderItem,
    ShippingTax,
    PaymentType,
    Address,
    User
)
from .forms import UserForm, LoginForm
import re

import json

def homepage(request):
    product_categories = ProductCategory.objects.values("id", "name")
    categories = []
    
    for category in product_categories:
        products = Product.objects.filter(product_category_id=category["id"])
        if len(products): categories.append(products)
    
    return render(request, "pages/homepage.html", {"categories": categories})

def signin(request):
    next_page = request.GET.get('next', "")
    context = {}
    if next_page:
        context["next_page"] = f"?next={next_page}"

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                if next_page:
                    return redirect(next_page)
                else:
                    return redirect("homepage")

            else:
                login_form.add_error(None, "E-mail or password was incorrect.")
                context["form"] = login_form
                return render(request, "pages/signin.html", context)
        else:
            context["form"] = login_form
            return render(request, "pages/signin.html", context)

    return render(request, "pages/signin.html", context)

def signup(request):
    next_page = request.GET.get('next', "")
    context = {}
    if next_page:
        context["next_page"] = f"?next={next_page}"
    
    if request.method == "POST":
        user_form = UserForm(request.POST)
        print(request.POST.get("first_name"))

        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != "":
            try:
                validate_password(password, user=None, password_validators=None)
            except Exception as e:
                user_form.add_error("password", e)

        if confirm_password != password and confirm_password != "":
            user_form.add_error("confirm_password", "Password is not equal")

        if user_form.is_valid():
            username = create_username(
                user_form.data.get("first_name", ""), 
                user_form.data.get("last_name", "")
            )

            user = User.objects.create_user(
                username=username,
                email=user_form.data.get("email", ""),
                first_name=user_form.data.get("first_name", ""),
                last_name=user_form.data.get("last_name", ""),
                password=password,
            )
            user.save()

            user = authenticate(email=user_form.data.get("email", ""), password=password)

            if user is not None:
                login(request, user)
                
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect("profile")
        else:
            context["form"] = user_form
            return render(request, "pages/signup.html", context)

    return render(request, "pages/signup.html", context)

def create_username(fn, ln):
    random_number = get_random_string(length=6, allowed_chars='0123456789')
    return f"{fn[:2]}{ln[:2]}{random_number}".upper()

def logout_view(request):
    logout(request)
    return redirect("signin")

@login_required
def account(request):
    return render(request, "pages/account.html")

@login_required
def profile(request):
    return render(request, "pages/profile.html")

@login_required
def order(request):
    context = {}
    
    try:
        print(request.user)
        address = Address.objects.get(user=request.user)
        context["address"] = address
    except Address.DoesNotExist:
        address = None
        
    if request.method == "POST":
        cart = json.loads(request.POST.get("cart")) # id, price, count(quantity), discount
        is_delivery = request.POST.get("is_delivery", False) == 'true'
        payment_code = request.POST.get("payment_type")
        
        order = Order()
        order.user = request.user
        payment_type = PaymentType.objects.get(code=payment_code)
        order.payment_type = payment_type
        
        if is_delivery:
            # find tax by Address model
            shipping_tax = ShippingTax.objects.get(pk=1)
            order.shipping_tax = shipping_tax
            order.shipping_tax_name = shipping_tax.name
            order.shipping_tax_value = shipping_tax.value
            
            if not address:
                address = Address()
                address.user = request.user
                address.cep = re.sub(r"\D", "", request.POST.get("cep"))
                address.district = request.POST.get("district")
                address.address = request.POST.get("address")
                address.complement = request.POST.get("complement")
                
                number = request.POST.get("number")
                if number: address.number = int(number)
                
                address.save()
        
        
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