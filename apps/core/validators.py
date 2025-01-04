from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from delivery.utils import remove_non_numeric

def cep_validator(value: str):
    if not value.isnumeric():
        raise ValidationError(
            _("Only digit characters."),
            params={"value": value},
        )
    elif len(value) != 8:
        raise ValidationError(
            _("Must have 8 digits."),
            params={"value": value},
        )
    

def name_validator(value: str):
    if not value.isalpha():
        raise ValidationError(
            _("Must contain only letters."),
            params={"value": value},
        )
    elif len(value) < 3:
        raise ValidationError(
            _("Minimum of 3 letters."),
            params={"value": value},
        )
        
def phone_validator(value: str):
    number = remove_non_numeric(value)
    
    if not number.isnumeric():
        raise ValidationError(
            _("Only digit characters."),
            params={"value": number},
        )
    elif len(number) < 10:
        raise ValidationError(
            _("Minimum of 10 digits."),
            params={"value": number},
        )
    elif len(number) > 11:
        raise ValidationError(
            _("Maximum of 11 digits."),
            params={"value": number},
        )
    elif len(number) == 11 and number[2] != "9":
        raise ValidationError(
            _("The third digit must be 9."),
            params={"value": number},
        )

def cellphone_number(value: str):
    number = remove_non_numeric(value)
    
    if not number.isnumeric():
        raise ValidationError(
            _("Only digit characters."),
            params={"value": number},
        )
    elif len(number) != 11:
        raise ValidationError(
            _("Must have 11 digits."),
            params={"value": number},
        )
    elif number[2] != "9":
        raise ValidationError(
            _("The third digit must be 9."),
            params={"value": number},
        )

def telephone_number(value: str):
    number = remove_non_numeric(value)
    
    if not number.isnumeric():
        raise ValidationError(
            _("Only digit characters."),
            params={"value": number},
        )
    elif len(number) != 10:
        raise ValidationError(
            _("Must have 10 digits."),
            params={"value": number},
        )
        
def cart_validator(cart):
    for item in cart:
        required_keys = ("id", "price", "count")
        for key in required_keys:
            if not key in item.keys():
                raise ValidationError(
                    _(f'The key "{key}" is required.'),
                    params={"value": key},
                )
                
def cpf_validator(value:str):
    numbers = [int(digit) for digit in value if digit.isdigit()]

    # Verifica se o CPF possui 11 números:
    if len(numbers) != 11:
        raise ValidationError(
            _("Must have 11 digits."),
            params={"value": numbers},
        )
    
    # Verifica se todos são iguais:
    if len(set(numbers)) == 1:
        raise ValidationError(
            _("All digits are equal."),
            params={"value": numbers},
        )

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValidationError(
            _("This CPF is invalid."),
            params={"value": numbers},
        )

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValidationError(
            _("This CPF is invalid."),
            params={"value": numbers},
        )
