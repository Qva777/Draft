from django.core.exceptions import ValidationError


def validate_negative(value):
    """
    Validator function to check the product price/count and set the 'active' field accordingly.
    """
    if value < 0:
        raise ValidationError('Quantity cannot be negative.')
    elif value == 0:
        active = False
    else:
        active = True
    return active


