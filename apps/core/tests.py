from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.core.validators import (name_validator, phone_validator, cep_validator)
from netdelivery.utils import first_occurrence

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
        
    def test_first_occurrence(self):
        uf = "RJ"
        no_lines = []
        self.assertEqual(first_occurrence(no_lines, uf), -1)
        
        one_line_without_match = ["6787@PR@Tuneiras do Oeste@87450000@0@M@@Tuneiras Oeste@4127908"]
        one_line_with_match = ["6870@RJ@Bom Jardim@28660000@0@M@@Bom Jardim@3300506"]
        
        self.assertEqual(first_occurrence(one_line_without_match, uf), -1)
        self.assertEqual(first_occurrence(one_line_with_match, uf), 0)
        
        two_lines_without_match = ["6788@PR@Tupãssi@85945000@0@M@@Tupãssi@4127957","6789@PR@Tupinambá@86746000@0@D@5798@Tupinambá@" ]
        two_lines_with_match_0_1_index = ["6873@RJ@Cabo Frio@@1@M@@Cb Frio@3300704","6874@RJ@Cabuçu@@2@D@6941@Cabuçu@"]
        two_lines_with_match_0_index = ["6874@RJ@Cabuçu@@2@D@6941@Cabuçu@", "7297@RN@Tibau@59678000@0@M@@Tibau@2411056"]
        two_lines_with_match_1_index = ["6788@PR@Tupãssi@85945000@0@M@@Tupãssi@4127957","6874@RJ@Cabuçu@@2@D@6941@Cabuçu@"]
        
        self.assertEqual(first_occurrence(two_lines_without_match, uf), -1)
        self.assertEqual(first_occurrence(two_lines_with_match_0_1_index, uf), 0)
        self.assertEqual(first_occurrence(two_lines_with_match_0_index, uf), 0)
        self.assertEqual(first_occurrence(two_lines_with_match_1_index, uf), 1)