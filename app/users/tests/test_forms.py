import pytest
from django.test import TestCase

from users.forms import UserSignInForm, UserSignUpForm
from users.models import User


class FormTest(TestCase):
    """Test cases for user-related forms"""

    @pytest.mark.django_db
    def test_user_signin_form_valid(self) -> None:
        """Test that the UserSignInForm is valid with correct data."""
        User.objects.create_user(email='test@example.com', password='testpassword')
        form = UserSignInForm(data={'email': 'test@example.com', 'password': 'testpassword'})

        assert form.is_valid()

    @pytest.mark.django_db
    def test_user_signup_form_valid(self) -> None:
        """Test that the UserSignUpForm is valid with correct data."""
        form = UserSignUpForm(
            data={
                'email': 'test@example.com',
                'password1': 'testpassword',
                'password2': 'testpassword',
            },
        )

        assert form.is_valid()

    @pytest.mark.django_db
    def test_user_signin_form_invalid(self) -> None:
        """Test that the UserSignInForm is invalid with incorrect data."""
        form = UserSignInForm(data={'email': 'test@example.com', 'password': 'invalidpassword'})

        assert not form.is_valid()

    @pytest.mark.django_db
    def test_user_signup_form_password_mismatch(self) -> None:
        """Test that the UserSignUpForm is invalid when passwords do not match."""
        form = UserSignUpForm(
            data={
                'email': 'test@example.com',
                'password1': 'testpassword',
                'password2': 'testpassworT',
            },
        )

        assert not form.is_valid()
        assert 'password2' in form.errors
