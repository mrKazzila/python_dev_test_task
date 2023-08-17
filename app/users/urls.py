from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (UserProfileView, UserSignInView, UserSignUpView)

app_name = 'users'

urlpatterns = [
    path('signin/', UserSignInView.as_view(), name='signin'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
