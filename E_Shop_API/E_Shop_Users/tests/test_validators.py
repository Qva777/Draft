from datetime import datetime
from unittest import TestCase
from django.core.exceptions import ValidationError

from E_Shop_API.E_Shop_Users.tests.enums.user_enums import UserErrorMessages
from E_Shop_API.E_Shop_Users.validators import birthday_validator, validate_password


class BirthdayValidatorTest(TestCase):
    """ Testing Birthday Validator """

    # test variable
    correct_date = datetime.now().strftime('%Y-%m-%d')
    incorrect_date = datetime.now().strftime('%m-%y-%d')

    def test_correct_date_format(self):
        """ Checking the correct date format """
        self.assertIsNone(birthday_validator(datetime.strptime(self.correct_date, "%Y-%m-%d").date()))

    def test_incorrect_date_format(self):
        """ Checking the wrong date format """
        with self.assertRaises(ValueError):
            birthday_validator(datetime.strptime(self.incorrect_date, "%Y-%m-%d").date())

    def test_future_date(self):
        """ Checking the future date format """
        with self.assertRaises(ValidationError):
            birthday_validator(datetime.strptime('2050-12-31', "%Y-%m-%d").date())

    def test_less_1930(self):
        """ Checking the date format less 1930-01-01 """
        with self.assertRaises(ValidationError):
            birthday_validator(datetime.strptime('1920-01-01', "%Y-%m-%d").date())


class PasswordValidatorTest(TestCase):
    """ Testing Password Validator """

    def test_short_password(self):
        """  Checking if the password to short """
        with self.assertRaises(ValidationError):
            validate_password('short')

    def test_password_without_numbers(self):
        """  Checking if the password without numbers """
        with self.assertRaises(ValidationError):
            validate_password('PasswordWithoutNumbers')

    def test_password_without_capital_letters(self):
        """  Checking if the password without upper letters """
        with self.assertRaises(ValidationError):
            validate_password('passwordwithoutcapitalletters')

    def test_valid_password(self):
        """ Should not raise any exception for a valid password """
        try:
            validate_password('ValidPasswordWith1Capital')
        except ValidationError:
            self.fail("Invalid Password")
