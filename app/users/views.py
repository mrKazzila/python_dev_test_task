from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from users.forms import UserSignInForm, UserSignUpForm
from users.models import User


class UserSignUpView(TitleMixin, SuccessMessageMixin, CreateView):
    """Registration page."""

    model = User
    form_class = UserSignUpForm
    title = 'Flake review - Sign up'
    template_name = 'users/signup.html'
    success_message = 'You are successfully registered!'

    def get_success_url(self):
        print(f'{self.object.id}')
        print(f'{self.object.email}')
        return reverse('users:user_profile', args=(self.object.id,))


class UserSignInView(TitleMixin, LoginView):
    """Login page."""

    title = 'Flake review - Sign In'
    template_name = 'users/signin.html'
    authentication_form = UserSignInForm

    def get_success_url(self):
        print(self.request.user.id)
        return reverse('users:user_profile', args=(self.request.user.id,))


class UserProfileView(LoginRequiredMixin, TitleMixin, DetailView):
    """User profile page."""

    model = User
    title = 'Flake review - profile'
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.id
