from django.core.exceptions import ValidationError

from E_Shop_API.E_Shop_Products.tests.ErrorMessage.product_enums import ProductErrorMessages


def validate_negative(value):
    """ Validator function to check the product price/count and set the 'active' field accordingly """
    if value < 0:
        raise ValidationError(ProductErrorMessages.NEGATIVE_VALUE)  # ?
    elif value == 0:
        active = False
    else:
        active = True
    return active
