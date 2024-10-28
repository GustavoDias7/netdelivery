from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password
from apps.user.models import User
from apps.order.models import (
    Order,
    OrderItem,
    ShippingFee,
    PaymentType,
    OrderItemStatus,
    WhiteListBairro,
    OrderAddress
)
from apps.address.models import (
    Logradouro,
    WhiteListUF,
    WhiteListLocalidade,
)
from apps.product.models import (
    Combo,
    Product,
    ProductVariant,
    Category
)
from django.core.paginator import Paginator
from apps.user.forms import UserForm, LoginForm
from apps.core import forms
from apps.core.utils import remove_non_alphanumeric
from apps.core.validators import cart_validator
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
import json
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

def header_categories(request):
    context = {
        "header_categories": [],
        "header_combos": False
    }
    qs_categories = Category.objects.all()
    
    for category in qs_categories:
        variant = ProductVariant.objects.filter(archived=False, product__category=category).first()
        if variant: context["header_categories"].append(variant.product.category)
        
    qs_combos = Combo.objects.filter(archived=False).first()
    if qs_combos: context["header_combos"] = True
    
    return context

def homepage(request):
    queryset_variants = ProductVariant.objects.filter(archived=False, default=True)
    categories = {}
    for variant in queryset_variants:
        category = variant.product.category.name
        if categories.get(category) == None:
            categories[category] = []
        categories[category].append(variant)
    
    queryset_combos = Combo.objects.filter(archived=False)
    combos = []
    for combo in queryset_combos:
        combos.append(combo)
        
    context = {
        "categories": categories,
        "combos": combos
    }
    
    return render(request, "pages/homepage.html", context)

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
        pass
        # address = Address.objects.get(user=request.user)
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
        # address = Address.objects.get(user=request.user)
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
        elif field == "number":
            num = None if request.POST.get(field) == "" else request.POST.get(field)
            data[field] = int(num) if num != None else num 
        elif field == "complement":
            comp = None if request.POST.get(field) == "" else request.POST.get(field)
            data[field] = comp
        
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
        
        if address and address.is_equal(field, form[field].value()):
            return redirect('address')
            
        if form.is_valid():
            if field == "cep":
                try:
                    log = Logradouro.objects.get(cep=data[field])
                    WhiteListUF.objects.get(uf=log.uf)
                    WhiteListLocalidade.objects.get(localidade=log.localidade)
                    WhiteListBairro.objects.get(bairro=log.bairro)
                except ObjectDoesNotExist:
                    context["field"].update({"value": form[field].value})
                    context["field"].update({"errors": "Não operamos neste endereço."})
                    return render(request, "pages/address_edit.html", context)
                
                if address == None:
                    address = None
                    # address = Address.objects.create(user=request.user)
                
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
        # address = Address.objects.get(user=request.user)
        context["address"] = address
        
        wl_bairro = WhiteListBairro.objects.get(bairro=address.logradouro.bairro)
        shippingfee = ShippingFee.objects.get(whitelistbairro=wl_bairro)
        context["shippingfee"] = shippingfee
    # except Address.DoesNotExist:
    #     address = None
    #     shippingfee = None
    except ShippingFee.DoesNotExist:
        try:
            shippingfee = ShippingFee.objects.get(is_default=True)
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
            
            try:
                if address.order_address:
                    order.order_address = address.order_address
                else:
                    raise ObjectDoesNotExist()
            except ObjectDoesNotExist:
                order_address = OrderAddress()
                order_address.set(address)
                order_address.save()
                
                order.order_address = order_address
                
                address.order_address = order_address
                address.save()
        
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