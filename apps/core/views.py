from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from apps.user.models import User
from apps.product.models import (
    Combo,
    ProductVariant,
)
from apps.user.forms import (UserForm, LoginForm)
from apps.core import forms
from apps.core.utils import (remove_non_alphanumeric, create_username)
# from django.core.exceptions import ObjectDoesNotExist

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
