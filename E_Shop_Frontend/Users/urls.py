from django.urls import path
from django.contrib.auth import views as auth_views
from E_Shop_Frontend.Users.views import UserLoginView, RegistrationView, DeletePhotoView, \
    EditProfileView

urlpatterns = [
    # Signup
    path('registration/', RegistrationView.as_view(), name='registration'),

    # Login/Logout
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Your Profile
    # path('profile/', edit_profile, name='user_profile'),

    path('profile/', EditProfileView.as_view(), name='user_profile'),

    path('profile/delete_photo/', DeletePhotoView.as_view(), name='delete_photo'),

]
