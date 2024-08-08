from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import (name_validator, phone_validator, cep_validator)

# Create your tests here.
class ValidatorsTestCase(TestCase):
    def test_name_validator(self):
        less_then_three_letters = "ab"
        alphanumeric = "Viniccius13"
        with_space = "c c"
        
        self.assertRaises(ValidationError, name_validator, value=less_then_three_letters)
        self.assertRaises(ValidationError, name_validator, value=alphanumeric)
        self.assertRaises(ValidationError, name_validator, value=with_space)
        
    def test_phone_validator(self):
        telephone_number = ["(21) 4002-8922", "2140028922"]
        with_letter = ["(21) 90000-000A", "2190000000A"]
        less_then_eleven_digits = ["(21) 4002", "214002"]
        eleven_digits_without_nine = ["(21) 00000-0000", "21000000000"]
        
        for number in telephone_number:
            self.assertRaises(ValidationError, phone_validator, value=number)
            
        for number in with_letter:
            self.assertRaises(ValidationError, phone_validator, value=number)
        
        for number in less_then_eleven_digits:
            self.assertRaises(ValidationError, phone_validator, value=number)
        
        for number in eleven_digits_without_nine:
            self.assertRaises(ValidationError, phone_validator, value=number)
            
    
    def test_cep_validator(self):
        with_dash = "96418-200"
        alphanumeric = "9641820A"
        less_then_eight_digits = "9641820"
        empty_string = ""
        
        self.assertRaises(ValidationError, cep_validator, value=with_dash)
        self.assertRaises(ValidationError, cep_validator, value=alphanumeric)
        self.assertRaises(ValidationError, cep_validator, value=less_then_eight_digits)
        self.assertRaises(ValidationError, cep_validator, value=empty_string)