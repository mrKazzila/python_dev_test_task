import logging
from pathlib import Path

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from code_checker.models import CheckLog, CodeCheck, CodeCheckStatus
from code_checker.utils import run_flake8
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


def check_user_files(uploaded_files):
    checked_files = []
    code_checker_objects = []

    for file_ in uploaded_files:
        code_check_obj = CodeCheck.objects.filter(file=file_).first()
        code_check_obj_id = code_check_obj.id

        CodeCheck.objects.filter(id=code_check_obj_id).update(is_notified=False)
        code_checker_objects.append(code_check_obj_id)

        if any(
            [
                code_check_obj.status == CodeCheckStatus.UNCHECKED.value,
                code_check_obj.status == CodeCheckStatus.IN_CHECKING.value,
            ],
        ):

            CodeCheck.objects.filter(id=code_check_obj_id).update(status=CodeCheckStatus.IN_CHECKING.value)

            absolute_file_path, file_name = _generate_path_to_user_file(file_obj=file_)
            logger.debug(f'Work with file: {absolute_file_path=}')

            return_code, stdout_, stderr_ = run_flake8(file_path=absolute_file_path)
            checked_files.append(file_name)

            CheckLog.objects.create(
                code_check=code_check_obj,
                log_text=f'Code check for file {file_name} with state {file_.state} is done!',
            )

            if stderr_ == '':
                logger.debug(f'RESULT return_code: {return_code}')
                logger.debug(f'RESULT stdout: {stdout_}')
                CodeCheck.objects.filter(id=code_check_obj_id).update(
                    status=CodeCheckStatus.DONE.value,
                    timestamp=timezone.now(),
                    last_check_result=stdout_,
                )

                file_.state = FileState.OLD.value

            else:
                logger.debug(f'RESULT stderr: {stderr_}')
                CodeCheck.objects.filter(id=code_check_obj_id).update(status=CodeCheckStatus.UNCHECKED.value)

            logger.debug(f'END FILE {file_name} STATUS {code_check_obj.status}')

            file_.save()

    messages_for_email = _generate_message_for_email(files=checked_files)
    return messages_for_email, code_checker_objects


def _generate_path_to_user_file(file_obj):
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


def _generate_message_for_email(files):
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
    if len(files) == 1:
        checked_files = ''.join(files)
        file_info = f'file {checked_files}'
    else:
        checked_files = ', '.join(files)
        file_info = f'files {checked_files}'

    return file_info
