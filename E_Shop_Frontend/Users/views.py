from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator

from E_Shop_API.E_Shop_Users.models import Clients
from .forms import UserEditForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import UserRegistrationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserEditForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserEditForm, UserRegistrationForm


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'
    form_class = UserEditForm
    success_url = 'user_profile'
    login_url = 'login'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Validate the current password

            # Update the password if a new one was provided
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)
                messages.success(request, 'Your password was successfully updated!')

            # Save the rest of the form fields
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(self.success_url)
        else:
            messages.error(request, 'There was an error updating your profile.')
            return render(request, self.template_name, {'form': form})


# class EditProfileView(LoginRequiredMixin, FormView):
#     template_name = 'user_profile.html'
#     form_class = UserEditForm
#     success_url = reverse_lazy('login')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         # Validate the current password
#         current_password = form.cleaned_data.get('current_password')
#         if current_password and not self.request.user.check_password(current_password):
#             messages.error(self.request, 'Invalid current password.')
#             return super().form_invalid(form)
#
#         # Update the password if a new one was provided
#         new_password = form.cleaned_data.get('new_password')
#         if new_password:
#             self.request.user.set_password(new_password)
#             messages.success(self.request, 'Your password was successfully updated!')
#
#         # Save the rest of the form fields
#         form.save()
#         messages.success(self.request, 'Your profile was successfully updated!')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'There was an error updating your profile.')
#         return super().form_invalid(form)


# @login_required(login_url='login')
# def edit_profile(request):
#     """
#     View for editing user profile.
#     """
#     if request.method == 'POST':
#         form = UserEditForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             # Validate the current password
#
#             # Update the password if a new one was provided
#             new_password = form.cleaned_data.get('new_password')
#             if new_password:
#                 request.user.set_password(new_password)
#                 messages.success(request, 'Your password was successfully updated!')
#
#             # Save the rest of the form fields
#             form.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             return redirect('user_profile')
#         else:
#             messages.error(request, 'There was an error updating your profile.')
#     else:
#         form = UserRegistrationForm(instance=request.user)
#     return render(request, 'user_profile.html', {'form': form})


class RegistrationView(View):
    """ Registration new user /registration/"""
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # Login the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class DeletePhotoView(View):
    """ Delete the user's profile photo """

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request):
        user = request.user
        user.photo.delete()
        user.save()
        messages.success(request, 'Photo deleted successfully.')
        return redirect('user_profile')


class UserLoginView(View):
    """ Login as user /login/ """
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, self.template_name, {'form': form})
