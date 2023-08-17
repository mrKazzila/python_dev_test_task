import pytest
from django.db import IntegrityError
from django.test import TestCase

from users.models import User


class UserTest(TestCase):
    """Tests for User model."""

    def test_user_model_has_email_field(self) -> None:
        """Test that the User model has expected fields."""
        fields = [field.name for field in User._meta.get_fields()]

        assert 'id' in fields
        assert 'email' in fields
        assert 'password' in fields
        assert 'is_active' in fields
        assert 'is_superuser' in fields
        assert 'is_staff' in fields

    @pytest.mark.django_db
    def test_user_str(self) -> None:
        """Test the __str__ method of the User model."""
        user = User.objects.create_user(email='mrrobot@example.com', password='testpassword')

        assert str(user) == 'mrrobot@example.com'

    @pytest.mark.django_db
    def test_user_can_be_created_with_email(self) -> None:
        """Test creating a user with email."""
        user = User.objects.create_user(email='mrrobot@example.com', password='password')

        assert user.email == 'mrrobot@example.com'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    @pytest.mark.django_db
    def test_create_user_no_email(self) -> None:
        """Test that creating a user with no email raises a ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_user(email=None, password='password')

    @pytest.mark.django_db
    def test_user_cannot_be_created_with_no_unique_email(self) -> None:
        """Test that creating a user with a non-unique email raises an IntegrityError."""
        User.objects.create_user(email='mrrobot@example.com', password='password')

        with pytest.raises(IntegrityError):
            User.objects.create_user(email='mrrobot@example.com', password='password')

    @pytest.mark.django_db
    def test_create_superuser(self) -> None:
        """Test creating a superuser."""
        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')

        assert admin_user.email == 'admin@example.com'
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_not_staff(self) -> None:
        """Test that creating a superuser with is_staff=False raises a ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpassword',
                is_staff=False,
            )

    @pytest.mark.django_db
    def test_create_superuser_not_superuser(self) -> None:
        """Test that creating a superuser with is_superuser=False raises a ValueError."""
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpassword',
                is_superuser=False,
            )
