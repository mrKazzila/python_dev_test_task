import logging

from code_checker.code_checker_services import (
    generate_check_log_massage,
    generate_path_to_user_file,
    get_new_or_overwritten_user_files,
)
from code_checker.models import CheckLog, CodeCheck, CodeCheckStatus
from code_checker.utils import run_flake8
from code_files.models import FileState, UploadedFile
from config.celery import app
from users.models import User

logger = logging.getLogger(__name__)

# def check_user_files(user, uploaded_files):
#     for file_ in uploaded_files:
#         code_check_obj = CodeCheck.objects.filter(file=file_).first()
#         logger.debug(f'FILE {file_} STATUS {code_check_obj.status}')
#
#         if code_check_obj.status == CodeCheckStatus.UNCHECKED.value:
#             file_path = generate_path_to_user_file(file_obj=file_)
#
#             code_check_obj.status = CodeCheckStatus.IN_CHECKING.value
#             return_code, stdout_, stderr_ = run_flake8(file_path=file_path)
#
#             if stderr_ == '':
#                 logger.info(f'RESULT return_code: {return_code}')
#                 logger.info(f'RESULT stdout: {stdout_}')
#                 code_check_obj.status = CodeCheckStatus.DONE.value
#                 file_.state = FileState.OLD.value
#
#             else:
#                 logger.info(f'RESULT stderr: {stderr_}')
#                 code_check_obj.status = CodeCheckStatus.UNCHECKED.value
#
#             logger.debug(f'END FILE {file_} STATUS {code_check_obj.status}')
#
#             code_check_obj.save()
#             file_.save()
#         else:
#             logger.info(f'No new Files for user: {user}')


@app.task
def run_flake8_checker():
    """Task for check upload files use flake8."""
    users = User.objects.all()

    for user in users:
        logger.info(f'Work with user: {user}')
        uploaded_files = get_new_or_overwritten_user_files(upload_file_model=UploadedFile, user=user)
        logger.info(f'Find: {uploaded_files}')

        # check_user_files(user=user, uploaded_files=uploaded_files)

        for file_ in uploaded_files:
            code_check_obj = CodeCheck.objects.filter(file=file_).first()
            logger.debug(f'FILE {file_} STATUS {code_check_obj.status}')

            if any(
                [
                    code_check_obj.status == CodeCheckStatus.UNCHECKED.value,
                    code_check_obj.status == CodeCheckStatus.IN_CHECKING.value,
                ],
            ):

                code_check_obj.status = CodeCheckStatus.IN_CHECKING.value
                code_check_obj.save()

                absolute_file_path, file_name = generate_path_to_user_file(file_obj=file_)
                logger.info(f'Work with file: {absolute_file_path=}')

                return_code, stdout_, stderr_ = run_flake8(file_path=absolute_file_path)

                check_log_massage = generate_check_log_massage(
                    file_name=file_name,
                    file_state=file_.state,
                    result_status_code=return_code,
                    result_report=stdout_,
                    result_errors=stderr_,
                )

                CheckLog.objects.update_or_create(code_check=code_check_obj, log_text=check_log_massage)
                logger.info(f'Generate CheckLog with massage {check_log_massage}')  # down to debug

                if stderr_ == '':
                    logger.info(f'RESULT return_code: {return_code}')
                    logger.info(f'RESULT stdout: {stdout_}')
                    code_check_obj.status = CodeCheckStatus.DONE.value
                    file_.state = FileState.OLD.value

                else:
                    logger.info(f'RESULT stderr: {stderr_}')
                    code_check_obj.status = CodeCheckStatus.UNCHECKED.value

                logger.debug(f'END FILE {file_name} STATUS {code_check_obj.status}')

                code_check_obj.save()
                file_.save()
            else:
                logger.info(f'No new Files for user: {user}')
