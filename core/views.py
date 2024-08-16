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
    ShippingFee,
    PaymentType,
    Address,
    User,
    OrderItemStatus,
    Logradouro
)
from django.core.paginator import Paginator
from core.forms import UserForm, LoginForm
from core import forms
import re
from core.utils import remove_non_alphanumeric


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
def edit(request):
    context = {}
    field = request.GET.get('field')

    if field == "": return redirect('profile')
    if field == "email": return redirect('profile')
    
    fields = {
        "first_name": "nome",
        "last_name": "sobrenome",
        # "email": "e-mail",
        "phone": "número de celular",
        "username": "nome de usuário",
    }
    
    if field not in fields: return redirect('profile')
    
    context["field"] = {}
    context["field"] = {
        "name": field,
        "label": fields[field],
        "value": request.user.get(field),
    }
    
    if request.method == "POST":
        data = {}
        if field == "phone":
            phone = request.POST.get(field)
            data[field] = remove_non_alphanumeric(phone)
        else:
            data[field] = request.POST.get(field)
        
        form = None
        match field:
            case "first_name":
                form = forms.FirstNameForm(data)
            case "last_name":
                form = forms.LastNameForm(data)
            case "phone":
                form = forms.PhoneForm(data)
            case "username":
                form = forms.UsernameForm(data)
            case _:
                print(None)
                
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.set(field, data[field])
            user.save()
            return redirect('profile')
        else:
            context["field"].update({"value": form[field].value})
            context["field"].update({"errors": form.errors.get(field).as_text})
        
    return render(request, "pages/edit.html", context)

@login_required
def orders(request):
    context = {}
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
def address(request):
    context = {}
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    context["address"] = address
    return render(request, "pages/address.html", context)

@login_required
def address_edit(request):
    
    context = {}
    field = request.GET.get('field')

    if field == "": return redirect('address')
    
    fields = {
        "cep": "CEP",
        "number": "número",
        "complement": "complemento",
    }
    
    if field not in fields: return redirect('address')
    
    context["field"] = {
        "name": field,
        "label": fields[field],
    }
    
    try:
        address = Address.objects.get(user=request.user)
        if field == "cep":
            context["field"]["value"] = address.logradouro.cep
        else: 
            context["field"]["value"] = address.get(field)
    except:
        address = None
    
    if request.method == "POST":
        data = {}
        
        if field == "cep":
            cep = request.POST.get(field)
            data[field] = remove_non_alphanumeric(cep)
        else: 
            data[field] = request.POST.get(field)
        
        form = None
        match field:
            case "cep":
                form = forms.CepForm(data)
            case "number":
                form = forms.NumberForm(data)
            case "complement":
                form = forms.ComplementForm(data)
            case _:
                print(None)
        
        context["form"] = form
        
        if form.is_valid():
            if field == "cep":
                try:
                    log = Logradouro.objects.get(cep=data[field])
                except Logradouro.DoesNotExist:
                    context["field"].update({"value": form[field].value})
                    context["field"].update({"errors": "Não operamos neste endereço."})
                    return render(request, "pages/address_edit.html", context)
                
                if address == None:
                    address = Address.objects.create(user=request.user)
                
                address.setLog(log)
            else:
                address.set(field, data[field] if data[field] else None)
                
            address.save()
            return redirect('address')
        else:
            context["field"].update({"value": form[field].value})
            context["field"].update({"errors": form.errors.get(field).as_text})
        
    return render(request, "pages/address_edit.html", context)

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
            shipping_fee = ShippingFee.objects.get(pk=1)
            order.shipping_fee = shipping_fee
            order.shipping_fee_name = shipping_fee.name
            order.shipping_fee_value = shipping_fee.value
            
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