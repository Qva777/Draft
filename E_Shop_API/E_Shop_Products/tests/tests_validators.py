# python manage.py test E_Shop_API.E_Shop_Products.tests.tests_validators
from django.test import TestCase
from django.core.exceptions import ValidationError
from E_Shop_API.E_Shop_Products.validators import validate_negative


class ValidatorsTestCase(TestCase):
    def test_validate_negative_positive_value(self):
        """ Should return True for positive values """
        result = validate_negative(10)
        self.assertTrue(result)

    def test_validate_negative_zero_value(self):
        """ Should return False for zero value """
        result = validate_negative(0)
        self.assertFalse(result)

    def test_validate_negative_negative_value(self):
        """ Should raise a ValidationError """
        with self.assertRaises(ValidationError):
            validate_negative(-10)
