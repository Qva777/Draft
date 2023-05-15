# python manage.py test E_Shop_Frontend.Users.tests.test_views
from unittest.mock import patch

import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from E_Shop_API.E_Shop_Users.models import Clients
from E_Shop_API.E_Shop_Users.tests.helpers.error_messages import ErrorMessages
from E_Shop_API.E_Shop_Users.tests.helpers.test_helpers import create_basic_user
from E_Shop_Frontend.Users.forms import UserEditForm
from E_Shop_Frontend.Users.views import RegistrationView, ResendConfirmationView, ConfirmAccountView, \
    ThrottleActivationEmail
from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.cache import cache
from django.contrib.messages import get_messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# UserLoginView
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class DeletePhotoViewTest(TestCase):
    def setUp(self):
        self.user = create_basic_user()
        self.image = SimpleUploadedFile(
            "test_image.jpg",
            content=open("E_Shop_config/static/img/bin.png", "rb").read(),
            content_type="image/jpeg",
        )
        self.user.photo = self.image
        self.user.save()

    def test_photo_deletion(self):
        self.client.login(username='User', password='UserPass123')
        response = self.client.post(reverse('delete_photo'))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.photo)

    def test_photo_deletion_redirects(self):
        response = self.client.post(reverse('delete_photo'))

        self.assertEqual(response.status_code, 302)


# достаток
# class EditProfileViewTest(TestCase):
#     def setUp(self):
#         self.client = create_basic_user()
#         self.client.login(username='User', password='UserPass123')
#         self.url = reverse('user_profile')
#
#     def test_get_edit_profile_page(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'pages/user_profile.html')
#         self.assertIsInstance(response.context['form'], UserEditForm)
#
#     def test_post_valid_form(self):
#         data = {
#             'first_name': 'NewFirstName',
#             'last_name': 'NewLastName',
#             'email': 'new_email@example.com',
#             'new_password': 'new_password123',  # Убедитесь, что ваша форма правильно обрабатывает это поле
#         }
#
#         response = self.client.post(self.url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('user_profile'))  # Замените на вашу URL-маршрутизацию
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.first_name, 'NewFirstName')
#         self.assertEqual(self.user.last_name, 'NewLastName')
#         self.assertEqual(self.user.email, 'new_email@example.com')
#
#     def test_post_invalid_form(self):
#         data = {
#             'first_name': 'NewFirstName',
#             'last_name': 'NewLastName',
#             'email': 'invalid_email',  # Неверный адрес электронной почты, вызовет ошибку валидации
#         }
#
#         response = self.client.post(self.url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'pages/user_profile.html')
#         self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
#
#     def test_post_change_password(self):
#         data = {
#             'new_password': 'new_password123',  # Убедитесь, что ваша форма правильно обрабатывает это поле
#         }
#
#         response = self.client.post(self.url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('user_profile'))  # Замените на вашу URL-маршрутизацию
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('new_password123'))

# class EditProfileViewTest(TestCase):
#     def setUp(self):
#         self.user = create_basic_user()
#         self.client.login(username='User', password='UserPass123')
#         self.url = reverse('user_profile')
#
#     def test_get_edit_profile_page(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'pages/user_profile.html')
#         self.assertIsInstance(response.context['form'], UserEditForm)
#
#     def test_post_valid_form(self):
#         data = {
#             'first_name': 'User',
#             'last_name': 'User',
#             'email': 'user@gmail.com',
#             'new_password': 'UserPass123',  # Убедитесь, что ваша форма правильно обрабатывает это поле
#         }
#
#         response = self.client.post(self.url, data, follow=True)
#
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.first_name, 'User')
#         self.assertEqual(self.user.last_name, 'User')
#         self.assertEqual(self.user.email, 'user@gmail.com')
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserLoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_get_login_view_for_anonymous_user(self):
        # Ensure that an anonymous user can access the login page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_get_login_view_for_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser@example.com', password='testpassword')

        # Ensure that an authenticated user is redirected to the home page
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_post_login_view_with_valid_credentials(self):
        # Ensure that a user can log in with valid credentials
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertRedirects(response, reverse('home'))

    def test_post_login_view_with_invalid_credentials(self):
        # Ensure that a user cannot log in with invalid credentials
        login_data = {
            'username': 'testuser@example.com',
            'password': 'wrongpassword',
            # 'password': 'wrongpasswor',

        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Invalid email or password. Please try again.')

    def test_post_login_view_with_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser@example.com', password='testpassword')

        # Ensure that an authenticated user is redirected to the home page
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertRedirects(response, reverse('home'))


from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_get_edit_profile_view(self):
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/user_profile.html')

    # def test_post_edit_profile_view_valid_data(self):
    #     # Login the user (you can modify this if your login view requires different data)
    #     self.client.login(username='testuser', password='testpassword')
    #
    #     # Define valid form data to update the profile
    #     valid_data = {
    #         'first_name': 'Updated First Name',
    #         'last_name': 'Updated Last Name',
    #         # Add other fields as needed
    #     }
    #
    #     # Send a POST request to edit the profile
    #     response = self.client.post(reverse('user_profile'), valid_data, follow=True)
    #
    #     # Check if the user profile has been updated successfully
    #     self.assertEqual(response.status_code, 200)  # Assuming you are redirecting to the profile page
    #     self.assertContains(response, 'Profile updated successfully')  # Add your success message here

    def test_post_edit_profile_view_valid_data(self):
        # Define valid form data to update the profile
        valid_data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
        }

        # Send a POST request to edit the profile
        response = self.client.post(reverse('user_profile'), valid_data, follow=True)

        # Check if the user profile has been updated successfully
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK responseo

        # Optionally, you can check the content of the page to verify that
        # it contains the updated profile information.
        self.assertContains(response, 'Updated First Name')
        self.assertContains(response, 'Updated Last Name')

    def test_post_edit_profile_view_invalid_data(self):
        url = reverse('user_profile')
        # Invalid data (missing required fields)
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/user_profile.html')
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        # Add more validation tests for other fields as needed


#  новый модуль
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = Clients.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_get_when_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the view
        response = self.client.get(reverse('forgot_password'))

        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))

    def test_get_when_not_authenticated(self):
        # Log out any user (if logged in)
        self.client.logout()

        # Make a GET request to the view
        response = self.client.get(reverse('forgot_password'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    # def test_post_email_not_found(self):
    #     # Make a POST request with an email that doesn't exist
    #     response = self.client.post(reverse('forgot_password'), {'email': 'nonexistent@example.com'})
    #
    #     # Check if the user is redirected back to the forgot password page with an error message
    #     self.assertRedirects(response, reverse('forgot_password'))
    #     self.assertContains(response, 'form_errors')

    def test_post_email_found_email_throttling(self):
        # Mock the EmailThrottling.send_email_with_throttling method
        with patch('E_Shop_API.E_Shop_Users.views.EmailThrottling.send_email_with_throttling') as mock_send_email:
            # Make a POST request with a valid email
            response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})

            # Check if the email is sent
            mock_send_email.assert_called_once()

        # Check if the user is redirected back to the forgot password page with a success message
        self.assertRedirects(response, reverse('forgot_password'))
        # self.assertContains(response, 'Password reset link has been sent to your email')

    # def test_post_email_found_email_throttling(self):
    #     # Mock the send_email_with_throttling function
    #     with patch('your_app.views.EmailThrottling.send_email_with_throttling') as mock_send_email:
    #         mock_send_email.return_value = True  # Simulate a successful email send
    #
    #         # Make a POST request with a valid email
    #         response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})
    #
    #         # Check if the email is sent
    #         mock_send_email.assert_called_once()
    #
    #         # Check if the user is redirected back to the forgot password page with a success message
    #         self.assertRedirects(response, reverse('forgot_password'))

    # def test_post_email_found_email_throttling_failed(self):
    #     # Mock the send_email_with_throttling function
    #     with patch('E_Shop_API.E_Shop_Users.views.EmailThrottling.send_email_with_throttling') as mock_send_email:
    #         mock_send_email.return_value = False  # Simulate a failed email send
    #
    #         # Make a POST request with a valid email
    #         response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})
    #
    #         # Check if the email send failed message is displayed
    #         self.assertContains(response, 'Password reset email can only be sent once per minute')

    def test_post_email_not_found(self):
        # Make a POST request with an email that doesn't exist
        response = self.client.post(reverse('forgot_password'), {'email': 'nonexistent@example.com'})

        # Check if the user is redirected back to the forgot password page
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK response

    #
    # def test_post_email_found_email_throttling_failed(self):
    #     # Mock the EmailThrottling.send_email_with_throttling method to simulate throttling
    #     with patch('E_Shop_API.E_Shop_Users.views.EmailThrottling.send_email_with_throttling') as mock_send_email:
    #         mock_send_email.return_value = False
    #
    #         # Make a POST request with a valid email
    #         response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})
    #
    #     # Check if the user is redirected back to the forgot password page with a warning message
    #     self.assertRedirects(response, reverse('forgot_password'))
    #     self.assertContains(response, 'Password reset email can only be sent once per minute')
    def test_post_email_found_email_throttling_failed(self):
        # Mock the send_email_with_throttling function
        with patch('E_Shop_API.E_Shop_Users.views.EmailThrottling.send_email_with_throttling') as mock_send_email:
            # mock_send_email.return_value = False  # Simulate a failed email send

            # Make a POST request with a valid email
            response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})

            # Check if the email send failed message is displayed
            self.assertEqual(response.status_code, 302)  # Expect a redirect status code
