from django.contrib.auth.models import AbstractUser, UserManager
import datetime
from datetime import date
from django.db import models

# from E_Shop_config.validators import validate_password


from django.core.exceptions import ValidationError
import re


#
# from E_Shop_Products.models import Product


def validate_password(value):
    if not re.search("[A-Z]", value):
        raise ValidationError("Password must contain at least one upper case letter.")
    if not re.search("[0-9]", value):
        raise ValidationError("Password must contain at least one digit.")
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")


# 4. Cart
#   https://django-shop.readthedocs.io/en/latest/reference/cart-checkout.html

# 5. Reset-code
#     a. code *
#     b. sent-to: (email) *
#     c. created_at *
#     d. updated_at
#     e. expires_at *


def validate_negative(value):
    if value < 0:
        raise ValidationError('Quantity %(value)s is not allowed', params={'value': value}, )


def birthday_validator(value):
    """Birthday Validator"""
    today = date.today()
    if value > today:
        raise ValidationError('Cannot be in the future.')
    elif value < datetime.datetime.strptime('1930-01-01', "%Y-%m-%d").date():
        raise ValidationError('This year is not valid. ')


class CustomManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с указанным именем, адресом электронной почты и паролем
        Create and save a user with the given username, email, and password."""
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", False)
    #     extra_fields.setdefault("is_superuser", False)
    #     return self._create_user(username, email, password, **extra_fields)
    #
    # def create_superuser(self, username, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #
    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError("Superuser must have is_staff=True.")
    #     if extra_fields.get("is_superuser") is not True:
    #         raise ValueError("Superuser must have is_superuser=True.")
    #
    #     return self._create_user(username, email, password, **extra_fields)


# def validate_count(value):
#     if value <= 0:
#         Product.active = False
#         return Product.active
#

# class FruitManager(models.Manager):
# def get_queryset(self):
# return super().get_queryset().filter(count__gt=0)
# class ProductFilter(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(count__gt=0)
#
#     def is_fruit_exists(self):
#         return self.count() > 0
#
#
# class ProductAdminFilter(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()


# class Product(models.Model):
#     """  Product models/fields  """
#     name = models.CharField(verbose_name='Name', max_length=64, blank=False, unique=True)
#     description = models.CharField(verbose_name='Description', max_length=255, blank=True)
#
#     photo = models.ImageField(verbose_name='Photo', max_length=255, upload_to='photos', blank=True)
#     price = models.FloatField(verbose_name='Price', validators=[validate_negative], max_length=100000, blank=False)
#     count = models.IntegerField(verbose_name='Count', validators=[validate_negative], blank=False)
#
#     created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
#     updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)
#     active = models.BooleanField(default=True, )
#
#     objects = ProductFilter()
#     admin_objects = ProductAdminFilter()
#
#     def __str__(self):
#         """Строковое представление"""
#         return self.name
#
#     class Meta:
#         verbose_name = 'Product'
#         verbose_name_plural = 'Products'


# class RoleType(models.TextChoices):
#     """      tttt        """
#     ADMIN = (1, "admin")
#     MANAGER = (2, "manager")
#     CUSTOMER = (3, "customer")


# class Role(models.Model):
#     """     type      """
#     # type = models.CharField(max_length=30, choices=RoleType.choices, default=RoleType.CUSTOMER, blank=False)
#
#     role = models.ManyToManyField('User_manager', verbose_name='Role', related_name="roles", blank=True)
#     # is_active = models.BooleanField(default=False)
#     # is_staff = models.BooleanField(default=False)
#     # is_superuser = False
#     created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
#     updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)

# def __str__(self):
#     """ String representation """
#     return self.type


# class UserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name,  password=None, birth_date=None, photo=None, disabled=False):
#         if not email:
#             raise ValueError("User must have an email")
#         if not password:
#             raise ValueError("User must have a password")
#
#         user = self.model(
#             email=self.normalize_email(email)
#         )
#         user.first_name = first_name
#         user.last_name = last_name
#
#         user.set_password(password)  # change password to hash
#         user.photo = photo
#         user.birth_date = birth_date
#         user.disabled = disabled
#         # user.active = is_active
#         user.save(using=self._db)
#         return user
#
# def create_superuser(self, email, first_name, last_name,  password=None, birth_date=None, photo=None, disabled=False,
# **extra_fields):
#     if not email:
#         raise ValueError("User must have an email")
#     if not password:
#         raise ValueError("User must have a password")
#
#     user = self.model(
#         email=self.normalize_email(email)
#     )
#     user.first_name = first_name
#     user.last_name = last_name
#     user.set_password(password)
#     user.photo = photo
#     user.birth_date = birth_date
#     user.disabled = disabled
#     user.admin = True
#     user.staff = True
#     user.active = True
#     user.save(using=self._db)
#     return user

# class Role(models.Model):
#     """     type      """
#     type = models.CharField(max_length=30, verbose_name='type ', blank=False)
#
#     # user = models.ManyToManyField(User_manager, verbose_name='Role', related_name="roles", blank=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
#     updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)

# def __str__(self):
#     """ String representation """
#     return str(self.user)


class User_manager(AbstractUser):  # Clients
    """ User models/fields """
    # username = None#models.CharField(verbose_name='Username', unique=True, max_length=64, blank=False)
    first_name = models.CharField(verbose_name='Name', max_length=64, blank=False)
    last_name = models.CharField(verbose_name='Surname', max_length=64, blank=False)

    email = models.EmailField(verbose_name='Email', unique=True, max_length=64, blank=False)
    #######################
    password = models.CharField(validators=[validate_password], verbose_name='Password', max_length=88, blank=False)
    #######################
    birth_date = models.DateField(verbose_name='Birthday', validators=[birthday_validator], blank=True,
                                  null=True)  # blank=False)
    photo = models.ImageField(verbose_name='Photo', max_length=255, upload_to='photos', null=True, blank=True)
    disabled = models.BooleanField(verbose_name='Disabled?', default=False, blank=True)

    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)

    # product = models.ManyToManyField(Product, verbose_name='Product', related_name="users", blank=True)
    # role = models.BooleanField(Role, verbose_name='Role', )
    # если ты админ то перейдя по ссылке админа ты можешь изменить суперюзера

    # is_active = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    #   card = models.ManyToManyField(Role, verbose_name='card', related_name="managers", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password', 'birth_date', 'disabled', 'photo']

    # REQUIRED_FIELDS = ['first_name', 'last_name',  'birth_date', 'disabled', 'username', 'email']

    # objects = CustomManager()
    # objects = UserManager()

    def __str__(self):
        """ String representation """
        return self.username

    class Meta:
        """ Representation in admin panel """
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        self.clean_fields(exclude=["photo"])
        super().save(*args, **kwargs)

# 5. Reset-code
#     a. code *
#     b. sent-to: (email) *
#     c. created_at *
#     d. updated_at
#     e. expires_at *
# class ResetCode(models.Model):
#     # code
#     sent_to = models.EmailField(verbose_name='Email', unique=True, max_length=64, blank=False)
#
#     created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=False)
#     updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)
# expires_at =


# 6. Payment
#     number of card
#     pin cod

# def card_validator(value):
#     """Birthday Validator"""
#     today = date.today()
# if value > today:
#     raise ValidationError('Cannot be in the future.')
# if value < datetime.datetime.strptime(today, "%Y-%m").date():
#     raise ValidationError('This year is not valid. ')


# class Payment(models.Model):
# number = models.IntegerField(verbose_name='Card Number', db_index=True, unique=True, max_length=15, blank=False)
# pin = models.IntegerField(verbose_name='Pin code', max_length=4, blank=False)
# cvv = models.IntegerField(verbose_name='CVV code', max_length=3, blank=False)
# expiration_date = models.DateField(verbose_name='Exp. Date', validators=[card_validator])
