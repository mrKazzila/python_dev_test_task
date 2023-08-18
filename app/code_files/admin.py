from django.contrib import admin

from code_files.models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """Register the UploadedFile model and settings fields for admin."""

    list_display = ('file',)
    fields = ('user', 'filename', ('is_new', 'is_checked'), 'uploaded_at')
