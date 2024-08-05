from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import (name_validator)

# Create your tests here.
class ValidatorsTestCase(TestCase):
    def test_name_validator(self):
        less_then_three_letters = "ab"
        alphanumeric = "Viniccius13"
        with_space = "c c"
        
        self.assertRaises(ValidationError, name_validator, value=less_then_three_letters)
        self.assertRaises(ValidationError, name_validator, value=alphanumeric)
        self.assertRaises(ValidationError, name_validator, value=with_space)