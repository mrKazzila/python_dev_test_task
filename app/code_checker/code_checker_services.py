import logging
from collections import namedtuple
from pathlib import Path

from django.conf import settings
from django.db.models import Prefetch
from django.utils import timezone

from code_checker.models import CheckLog, CodeCheck, CodeCheckStatus
from code_checker.utils import run_flake8
from code_files.models import FileState, UploadedFile
from users.models import User

logger = logging.getLogger(__name__)


def get_users_files_with_new_or_overwritten_state():
    """
    Retrieve a list of users along with their uploaded files that have a new or overwritten state.

    Returns:
        A queryset containing users and their filtered files with new or overwritten state.
    """
    users_with_files = User.objects.prefetch_related(
        Prefetch(
            'uploadedfile_set',
            queryset=UploadedFile.objects.filter(state__in=[FileState.NEW.value, FileState.OVERWRITTEN.value]),
            to_attr='filtered_files',
        ),
    ).distinct()

    return users_with_files


def check_user_files(uploaded_files):
    """
    Check user-uploaded files using the Flake8 code checker.

    Args:
        uploaded_files: A list of uploaded file objects.

    Returns:
        A named tuple with the fields 'message' and 'code_check_objects_id'.

            message: Email message containing information about the code check.
            code_check_objects_id: List of IDs of code check objects.
    """
    result = namedtuple('CheckResult', 'message, code_check_objects_id')

    checked_files = []
    code_checker_objects = []

    code_checks_to_process = CodeCheck.objects.filter(
        file__in=uploaded_files,
        status__in=[CodeCheckStatus.UNCHECKED.value, CodeCheckStatus.IN_CHECKING.value],
    )

    for code_check_obj in code_checks_to_process:

        code_check_obj.is_notified = False
        code_check_obj.status = CodeCheckStatus.IN_CHECKING.value
        code_check_obj.save()

        code_checker_objects.append(code_check_obj.id)

        absolute_file_path, file_name = _generate_path_to_user_file(file_obj=code_check_obj.file)
        logger.info(f'Work with file: {absolute_file_path=}')

        return_code, stdout_, stderr_ = run_flake8(file_path=absolute_file_path)
        checked_files.append(file_name)

        CheckLog.objects.create(
            code_check=code_check_obj,
            log_text=f'Code check for file {file_name} with state {code_check_obj.file.state} is done!',
        )

        if not stderr_:
            logger.debug(f'Result run_flake8 return_code: {return_code}')
            logger.debug(f'Result run_flake8 stdout: {stdout_}')

            code_check_obj.status = CodeCheckStatus.DONE.value
            code_check_obj.timestamp = timezone.now()
            code_check_obj.last_check_result = stdout_

            code_check_obj.file.state = FileState.OLD.value
        else:
            logger.debug(f'Result run_flake8 stderr: {stderr_}')
            code_check_obj.status = CodeCheckStatus.UNCHECKED.value

        code_check_obj.save()
        code_check_obj.file.save()

    messages_for_email = _generate_message_for_email(files=checked_files)

    return result(message=messages_for_email, code_check_objects_id=code_checker_objects)


def _generate_path_to_user_file(file_obj):
    """
    Generate the absolute file path and file name for a given file object.

    Args:
        file_obj: The file object for which the path and name are to be generated.

    Returns:
        A tuple containing the absolute file path and the file name.
    """
    absolute_file_path = Path(settings.MEDIA_ROOT / file_obj.file.name).resolve()
    file_name = file_obj.filename

    return absolute_file_path, file_name


def _generate_message_for_email(files):
    """
    Generate an email message containing information about checked files.

    Args:
        files: A list of filenames that were checked.

    Returns:
        The generated email message containing information about the checked files.
    """
    files_page = 'files/list/'
    file_info = _generate_str_with_checked_files(files)

    message = (
        f'We checked your code with flake8 for this {file_info}\n'
        f'You can checked result in page {settings.DOMAIN_NAME}{files_page}\n\n'
        f'Best regards!\n'
        f'Flake review team.\n'
    )

    return message


def _generate_str_with_checked_files(files):
    """
    Generate a string containing information about the checked files.

    Args:
        files: A list of filenames.

    Returns:
        The generated string with information about the checked files.
    """
    count_files = len(files)
    file_info = f'file {files[0]}.' if count_files == 1 else f'files: {", ".join(files)}.'

    return file_info
