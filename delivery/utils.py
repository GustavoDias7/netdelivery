from django.contrib import admin
from django.utils.crypto import get_random_string
from django.conf import settings
import os

def remove_non_numeric(value:str):
    return "".join(e for e in value if e.isdigit())

def remove_non_alphanumeric(value: str):
    return "".join([e for e in value if e.isalnum()])

def first_occurrence(lines, value):
    low = 0
    high = len(lines) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2
        uf = lines[mid].split("@")[1]

        if uf < value:
            low = mid + 1

        elif uf > value:
            high = mid - 1

        elif uf == value:
            if len(lines) == 1: return mid
            elif mid == 0: return mid
            elif lines[mid - 1].split("@")[1] != value: return mid
            else: high = mid - 1
                
 
    # If we reach here, then the element was not present
    return -1

def last_occurrence(lines, value):
    low = 0
    high = len(lines) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2
        uf = lines[mid].split("@")[1]

        if uf < value:
            low = mid + 1

        elif uf > value:
            high = mid - 1

        elif uf == value:
            if len(lines) == 1: return mid
            elif mid == 0: return mid
            elif len(lines) - 1 == mid: return mid
            elif lines[mid + 1].split("@")[1] != value: return mid
            else: low = mid + 1
                
 
    # If we reach here, then the element was not present
    return -1

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

def create_username(fn: str, ln: str) -> str:
    random_number = get_random_string(length=6, allowed_chars='0123456789')
    return f"{fn[:2]}{ln[:2]}{random_number}".upper()

def fphone_number(number: str) -> str:
    is_str = number and type(number) == str
    if is_str:
        ddd = number[0:2]
        
        if len(number) == 11:
            part1 = number[2:7]
            part2 = number[7:]
        else:
            part1 = number[2:6]
            part2 = number[6:]
        
        return f"({ddd}) {part1}-{part2}"
    else:
        return ""
    
def fcpf(cpf: str) -> str:
    if (cpf and type(cpf) == str):
        part1 = cpf[3:6]
        part2 = cpf[6:9]
        return f"***.{part1}.{part2}-**"
    else:
        return ""
    
    
def create_temp_file(f, filename: str):
    temp_folder = os.path.join(settings.BASE_DIR, "temp")
    temp_file = os.path.join(temp_folder, filename)
    
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
         
    with open(file=temp_file, mode="wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    