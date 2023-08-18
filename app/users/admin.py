from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Register the User model and settings fields for admin."""

    list_display = ('email',)
    fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser')
