from django.db import models

from users.models import User


def user_directory_path(instance, filename):
    """Create folder for user files."""
    return f'user_{instance.user.id}/code/{filename}'


class UploadedFile(models.Model):
    """Upload file model."""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to=user_directory_path)
    filename = models.CharField(max_length=80)
    is_new = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name
