from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Clients
from .validators import validate_password


# class RegistrationForm(UserCreationForm):
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={'required': 'required'}),
#         validators=[validate_password],
#         help_text="Password must contain at least one upper case letter, one digit, and be at least 8 characters long."
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={'required': 'required'})
#     )
#
#     class Meta:
#         model = Clients
#         fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1',  'photo')#'password2',
#
#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.birth_date = self.cleaned_data['birth_date']
#         if commit:
#             user.save()
#         return user
