from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """User manager for User model."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a regular user.

        Args:
            email: User's email address.
            password: User's password.
            extra_fields: Extra fields for the user.

        Returns:
            User: Created user object.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser.

        Args:
            email: Superuser's email address.
            password: Superuser's password.
            extra_fields: Extra fields for the superuser.

        Returns:
            User: Created superuser object.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    email = models.EmailField(verbose_name='Email', unique=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
