#  ######gg
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
import re
from E_Shop_API.E_Shop_Users.models import Clients
from E_Shop_API.E_Shop_Users.validators import validate_password


class ClientsCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), validators=[validate_password])
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    class Meta:
        model = Clients
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date', 'photo', 'disabled']
#  ######gg