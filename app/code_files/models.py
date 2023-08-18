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
        to=User,
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to=user_directory_path)
    filename = models.CharField(max_length=80)
    state = models.CharField(
        max_length=11,
        choices=[(state_.name, state_.value) for state_ in FileState],
        default=FileState.NEW.value,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class CodeCheckStatus(Enum):
    """Enum order statuses."""

    DONE = 'Done'
    IN_CHECKING = 'In checking'
    UNCHECKED = 'Unchecked'


class CodeCheck(models.Model):
    """Code Check model."""

    file = models.ForeignKey(
        to=UploadedFile,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=11,
        choices=[(status.name, status.value) for status in CodeCheckStatus],
        default=CodeCheckStatus.UNCHECKED.name,
    )


class CheckLog(models.Model):
    """Check log model."""

    code_check = models.ForeignKey(
        to=CodeCheck,
        on_delete=models.CASCADE,
    )
    log_text = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
