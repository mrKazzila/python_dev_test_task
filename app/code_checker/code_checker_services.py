import logging
from datetime import datetime
from pathlib import Path

from django.db.models import Q

from code_checker.models import CheckLog, CodeCheck, CodeCheckStatus
from code_checker.utils import run_flake8
from code_files.models import FileState
from config.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)


def check_user_files(uploaded_files):
    all_files_log_massages = []
    code_checker_objects = []

    for file_ in uploaded_files:
        code_check_obj = CodeCheck.objects.filter(file=file_).first()
        code_check_obj_id = code_check_obj.id
        logger.debug(f'FILE {file_} STATUS {code_check_obj.status}')

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

            check_log_message_for_file = _generate_check_log_message(
                file_name=file_name,
                file_state=file_.state,
                result_report=stdout_,
            )
            all_files_log_massages.append(check_log_message_for_file)

            CheckLog.objects.update_or_create(code_check=code_check_obj, log_text=check_log_message_for_file)
            logger.debug(f'Generate CheckLog with massage {check_log_message_for_file}')

            if stderr_ == '':
                logger.debug(f'RESULT return_code: {return_code}')
                logger.debug(f'RESULT stdout: {stdout_}')
                CodeCheck.objects.filter(id=code_check_obj_id).update(status=CodeCheckStatus.DONE.value)
                file_.state = FileState.OLD.value

            else:
                logger.debug(f'RESULT stderr: {stderr_}')
                CodeCheck.objects.filter(id=code_check_obj_id).update(status=CodeCheckStatus.UNCHECKED.value)

            logger.debug(f'END FILE {file_name} STATUS {code_check_obj.status}')

            file_.save()

    return '\n'.join(all_files_log_massages), code_checker_objects


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


def _generate_check_log_message(file_name, file_state, result_report):
    """
    Generate a log message containing information about the code check results.

    Args:
        file_name: The name of the checked file.
        file_state: The state of the checked file.
        result_report: The result report of the code check.

    Returns:
        A formatted log message with relevant information.
    """
    result = ' Without problems.' if result_report == '' else f'\n{result_report}'
    message = (
        f'{file_name}.\n'
        f'[{datetime.now()}] File state: {file_state}.\n'
        f'[{datetime.now()}] Checking result:{result}\n'
    )
    return message
