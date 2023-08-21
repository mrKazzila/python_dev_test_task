import httpretty
import pytest
from django.test import Client, TestCase
from django.urls import reverse

from users.forms import UserSignInForm, UserSignUpForm
from users.models import User


class BaseSetUp(TestCase):
    """Base test class with setup for common test cases."""

    def setUp(self) -> None:
        """Set up the client for testing."""
        self.client = Client()


class UserSignUpViewTest(BaseSetUp):
    """Test cases for the UserSignUpView."""

    @pytest.mark.django_db
    def test_user_signup(self) -> None:
        """Test user signup page rendering and form instance."""
        url = reverse('users:signup')
        response = self.client.get(url)

        assert response.status_code == 200
        assert isinstance(response.context['form'], UserSignUpForm)

    @pytest.mark.django_db
    def test_user_signup_success(self) -> None:
        """Test user signup page rendering and form instance."""
        url = reverse('users:signup')
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'g-recaptcha-response': 'test_response',
        }

        with httpretty.enabled():
            httpretty.register_uri(
                httpretty.POST,
                'https://www.google.com/recaptcha/api/siteverify',
                body='{"success": true}',
                content_type='application/json',
            )

            response = self.client.post(url, form_data)
            assert response.status_code == 302
            assert User.objects.filter(email='test@example.com').exists()


class UserSignIpViewTest(BaseSetUp):
    """Test cases for the UserSignInView."""

    @pytest.mark.django_db
    def test_user_signin_view(self) -> None:
        """Test user signin page rendering and form instance."""
        url = reverse('users:signin')
        response = self.client.get(url)

        assert response.status_code == 200
        assert isinstance(response.context['form'], UserSignInForm)

    @pytest.mark.django_db
    def test_user_signin_success(self) -> None:
        """Test successful user signin."""
        User.objects.create_user(email='test@example.com', password='testpassword')
        url = reverse('users:signin')

        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)

        assert response.status_code == 302
        assert response.url == reverse('code_files:file_list')


class UserProfileViewTest(BaseSetUp):
    """Test cases for the UserProfileView."""

    @pytest.mark.django_db
    def test_user_profile(self) -> None:
        """Test user profile page rendering and user details display."""
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_login(user)

        url = reverse('users:user_profile', args=[user.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.context['object'] == user.id
        assert str(response.context.get('user')) == user.email

    @pytest.mark.django_db
    def test_user_profile_displayed_only_auth_user_info(self) -> None:
        """Test that the user profile displays only the authorized user's information."""
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_login(user)
        wrong_user_id = user.id + 1

        url = reverse('users:user_profile', args=[wrong_user_id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.context['object'] == user.id
        assert str(response.context.get('user')) == user.email
