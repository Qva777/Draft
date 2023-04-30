from django.urls import path
from E_Shop_API.E_Shop_Users.views import MyUserView, UserDetailView, SiteView, SelectSocialApplicationView

urlpatterns = [
    # CRUD
    path('auth/users/me/', MyUserView.as_view(), name='my_user_view'),
    path('auth/users/<uuid:pk>/', UserDetailView.as_view(), name='user_detail_view'),

    # GOOGLE OAUTH PROVIDER
    path('sites/<int:pk>/', SiteView.as_view(), name='site_detail'),
    path('provider/<int:pk>/', SelectSocialApplicationView.as_view(), name='select_social_application'),
]
