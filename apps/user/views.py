from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from apps.user.models import User
from . import forms
from delivery.utils import (remove_non_alphanumeric, create_username)

# Create your views here.
def signin(request, username):
    next_page = request.GET.get('next', "")
    context = {"username": username}
    if next_page:
        context["next_page"] = f"?next={next_page}"

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)

        if login_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                if next_page:
                    return redirect(next_page, username)
                else:
                    return redirect("homepage", username)

            else:
                login_form.add_error(None, "E-mail or password was incorrect.")
                context["form"] = login_form
                return render(request, "pages/signin.html", context)
        else:
            context["form"] = login_form
            return render(request, "pages/signin.html", context)

    return render(request, "pages/signin.html", context)

def signup(request, username):
    next_page = request.GET.get('next', "")
    context = {"username": username}
    if next_page:
        context["next_page"] = f"?next={next_page}"
    
    if request.method == "POST":
        user_form = forms.UserForm(request.POST)

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
            new_username = create_username(
                user_form.data.get("first_name", ""), 
                user_form.data.get("last_name", "")
            )

            user = User.objects.create_user(
                username=new_username,
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
                    return redirect(next_page, username)
                else:
                    return redirect("profile", username)
        else:
            context["form"] = user_form
            return render(request, "pages/signup.html", context)

    return render(request, "pages/signup.html", context)

def logout_view(request, username):
    logout(request)
    return redirect("signin", username)

def account(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    return render(request, "pages/account.html", context)

def profile(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    return render(request, "pages/profile.html", context)

def edit(request, username):
    if not request.user.is_authenticated:
        return redirect(f"/{username}/login/?next={request.path}")
    context = {"username": username}
    field = request.GET.get('field')

    if field == "": return redirect('profile', username)
    if field == "email": return redirect('profile', username)
    
    is_owner = request.user.is_staff and request.user.owner == None
    if is_owner:
        if field == "username": return redirect('profile', username)
    
    fields = {
        "first_name": "nome",
        "last_name": "sobrenome",
        # "email": "e-mail",
        "phone": "número de celular",
    }
    
    is_regular_user = not request.user.is_staff
    not_owner = request.user.is_staff and request.user.owner
    if is_regular_user or not_owner:
        fields["username"] = "nome de usuário"
    
    if field not in fields: return redirect('profile', username)
    
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
            return redirect('profile', username)
        else:
            context["field"].update({"value": form[field].value})
            context["field"].update({"errors": form.errors.get(field).as_text})
        
    return render(request, "pages/edit.html", context)
