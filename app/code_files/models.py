from enum import Enum

from django.db import models

from users.models import User


def user_directory_path(instance, filename):
    """Create folder for user files."""
    return f'user_{instance.user.id}/code/{filename}'


class FileState(Enum):
    """Enum file states."""

    NEW = 'New'
    OVERWRITTEN = 'Overwritten'
    OLD = 'Old'


class UploadedFile(models.Model):
    """Upload file model."""

    user = models.ForeignKey(
        verbose_name='User',
        to=User,
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        verbose_name='File',
        upload_to=user_directory_path,
    )
    filename = models.CharField(
        verbose_name='Filename',
        max_length=80,
    )
    state = models.CharField(
        verbose_name='File state',
        max_length=11,
        choices=[(state_.name, state_.value) for state_ in FileState],
        default=FileState.NEW.value,
    )
    uploaded_at = models.DateTimeField(
        verbose_name='Uploaded At',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'

    def __str__(self):
        return self.file.name
