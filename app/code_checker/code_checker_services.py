import logging
from pathlib import Path

from django.db.models import Q
from datetime import datetime

from code_files.models import FileState
from config.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)


def get_new_or_overwritten_user_files(upload_file_model, user):
    """
    Retrieve files that are in the NEW or OVERWRITTEN state for a specific user.

    Args:
        upload_file_model: The model representing the uploaded files.
        user: The user for whom the files are to be retrieved.

    Returns:
        A queryset containing files in the NEW or OVERWRITTEN state for the specified user.
    """
    files = (
        upload_file_model.objects.
        filter(Q(user=user) & (Q(state=FileState.NEW.value) | Q(state=FileState.OVERWRITTEN.value)))
    )

    return files


def generate_path_to_user_file(file_obj):
    """
    Generate the absolute file path and file name for a given file object.

    Args:
        file_obj: The file object for which the path and name are to be generated.

    Returns:
        A tuple containing the absolute file path and the file name.
    """
    absolute_file_path = Path(MEDIA_ROOT / file_obj.file.name).resolve()
    file_name = file_obj.filename

    return absolute_file_path, file_name


def generate_check_log_massage(file_name, file_state, result_status_code, result_report, result_errors):
    massage = f'[{datetime.now()}] Done checking for {file_name} with state {file_state}\n' \
              f'[{datetime.now()}] Checking code {result_status_code}\n' \
              f'[{datetime.now()}] Checking result: {result_report}\n' \
              f'[{datetime.now()}] Checking errors: {result_errors}\n'

    return massage
