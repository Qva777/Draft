from django.urls import path, include
from E_Shop_API.E_Shop_Users.views import MyUserView, UserDetailView, SiteView, SelectSocialApplicationView

urlpatterns = [
    # CRUD
    path('auth/users/me/', MyUserView.as_view(), name='my_user_view'),
    path('auth/users/<uuid:pk>/', UserDetailView.as_view(), name='user_detail_view'),

    # GOOGLE
    path('sites/<int:pk>/', SiteView.as_view(), name='site_detail'),
    path('provider/<int:pk>/', SelectSocialApplicationView.as_view(), name='select_social_application'),


    # preparing to delete
    # path('auth/', include('djoser.urls')),
    # path('auth/token/', CustomTokenCreateView.as_view(), name='token_create'),
    # path('auth/users/', CustomUserViewSet.as_view({'post': 'create'}), name='user_create'),
    # path('auth/register/', MyUserCreateView.as_view(), name='register'),
    # path('auth/login/', MyTokenCreateView.as_view(), name='login'),

    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
]