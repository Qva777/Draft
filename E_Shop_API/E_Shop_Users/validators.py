import re
import datetime
from datetime import datetime, date
from django.core.exceptions import ValidationError


def validate_password(value):
    """ Password validator """
    if not re.search("[A-Z]", value):
        raise ValidationError("Password must contain at least one upper case letter.")
    if not re.search("[0-9]", value):
        raise ValidationError("Password must contain at least one digit.")
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")


def birthday_validator(value):
    """Birthday Validator"""
    # date_obj = datetime.strptime(value, "%Y-%m-%d").date()
    today = date.today()
    if value > today:
        raise ValidationError('Cannot be in the future.')
    elif value < datetime.strptime('1930-01-01', "%Y-%m-%d").date():
        raise ValidationError('This year is not valid. ')
