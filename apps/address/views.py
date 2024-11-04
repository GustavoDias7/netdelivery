from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.utils import remove_non_alphanumeric
from apps.address.models import (
    Logradouro,
    WhiteListUF,
    WhiteListLocalidade,
    WhiteListBairro
)
from django.core.exceptions import ObjectDoesNotExist
from . import forms


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


