from enum import Enum

from django.db import models

from code_files.models import UploadedFile


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
