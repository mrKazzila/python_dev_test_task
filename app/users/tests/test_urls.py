from django.contrib.auth.views import LogoutView
from django.test import TestCase
from django.urls import resolve, reverse

from users.models import User
from users.views import UserProfileView, UserSignInView, UserSignUpView


class UsersUrlsTest(TestCase):
    """Test cases for user-related URLs."""

    def test_user_profile_url(self) -> None:
        """Test that the user profile URL resolves to the correct view."""
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        path = reverse('users:user_profile', args=[user.id])

        assert resolve(path).func.view_class == UserProfileView

    def test_user_signin_url(self) -> None:
        """Test that the user signin URL resolves to the correct view."""
        path = reverse('users:signin')
        assert resolve(path).func.view_class == UserSignInView

    def test_user_signup_url(self) -> None:
        """Test that the user signup URL resolves to the correct view."""
        path = reverse('users:signup')
        assert resolve(path).func.view_class == UserSignUpView

    def test_logout_url(self) -> None:
        """Test that the logout URL resolves to the correct view."""
        path = reverse('users:logout')
        assert resolve(path).func.view_class == LogoutView
