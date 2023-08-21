from django.contrib import admin

from code_checker.models import CheckLog, CodeCheck


@admin.register(CodeCheck)
class CodeCheckAdmin(admin.ModelAdmin):
    """Register the CodeCheck model and settings fields for admin."""

    list_display = ('file',)
    fields = (
        ('file', 'timestamp'),
        ('status', 'is_notified'),
        'last_check_result',
    )


@admin.register(CheckLog)
class CheckLogAdmin(admin.ModelAdmin):
    """Register the CheckLog model and settings fields for admin."""

    list_display = ('code_check',)
    fields = ('code_check',)
