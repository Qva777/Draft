from django.urls import path
from django.contrib.auth import views as auth_views
from E_Shop_Frontend.Users import views

urlpatterns = [
    # Signup
    path('registration/', views.RegistrationView.as_view(), name='registration'),

    # Login/Logout
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Edit User Profile
    path('profile/', views.EditProfileView.as_view(), name='user_profile'),
    path('profile/delete_photo/', views.DeletePhotoView.as_view(), name='delete_photo'),

]
