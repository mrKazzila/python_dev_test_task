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
        verbose_name='Uploaded File',
        to=UploadedFile,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(
        verbose_name='Timestamp',
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name='Check status',
        max_length=11,
        choices=[(status.name, status.value) for status in CodeCheckStatus],
        default=CodeCheckStatus.UNCHECKED.name,
    )
    last_check_result = models.TextField(
        verbose_name='Last check result',
        max_length=8000,
        default='Without problems',
    )
    is_notified = models.BooleanField(
        verbose_name='User is notified by email',
        default=False,
    )

    class Meta:
        verbose_name = 'Code Check'
        verbose_name_plural = 'Code Checks'


class CheckLog(models.Model):
    """Check log model."""

    code_check = models.ForeignKey(
        verbose_name='Code Check',
        to=CodeCheck,
        on_delete=models.CASCADE,
    )
    log_text = models.TextField(
        verbose_name='Log message',
        max_length=8000,
    )
    created_at = models.DateTimeField(
        verbose_name='Created At',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Check Log'
        verbose_name_plural = 'Check Logs'
