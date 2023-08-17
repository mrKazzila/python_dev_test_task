from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from .forms import UserSignInForm, UserSignUpForm
from .models import User


class UserSignUpView(SuccessMessageMixin, CreateView):
    """Registration page"""

    model = User
    form_class = UserSignUpForm
    template_name = 'users/signup.html'
    success_message = 'You are successfully registered!'

    def get_success_url(self):
        print(f'{self.object.id}')
        print(f'{self.object.email}')
        return reverse('users:user_profile', args=(self.object.id,))


class UserSignInView(LoginView):
    """Login page"""

    template_name = 'users/signin.html'
    authentication_form = UserSignInForm

    def get_success_url(self):
        print(self.request.user.id)
        return reverse('users:user_profile', args=(self.request.user.id,))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.id
