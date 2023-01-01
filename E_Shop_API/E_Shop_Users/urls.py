from django.urls import path
from E_Shop_Users.views import MyUserView, UserDetailView

app_name = 'Users'
urlpatterns = [

    # CRUD
    path('auth/users/me/', MyUserView.as_view()),
    path('auth/users/<int:pk>/', UserDetailView.as_view()),  # permissions Is_admin
]
