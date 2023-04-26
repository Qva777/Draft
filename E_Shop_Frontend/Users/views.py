from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import UserEditForm, UserRegistrationForm


class RegistrationView(View):
    """ Registration new user /registration/ """
    form_class = UserRegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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


class UserLoginView(View):
    """ Login as user /login/ """
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        if request.user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
            return redirect('home')
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


class EditProfileView(LoginRequiredMixin, View):
    """ Edit the user's profile """
    template_name = 'pages/user_profile.html'
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
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                request.user.set_password(new_password)

            # Save the rest of the form fields
            form.save()
            return redirect(self.success_url)
        else:
            messages.error(request, 'There was an error updating your profile.')
            return render(request, self.template_name, {'form': form})


class DeletePhotoView(LoginRequiredMixin, View):
    """ Delete the user's profile photo """

    @staticmethod
    def post(request):
        user = request.user
        user.photo.delete()
        user.save()
        return redirect('user_profile')
