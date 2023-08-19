import logging
from pathlib import Path

from django.db.models import Q

from code_files.models import CodeCheck, CheckLog, CodeCheckStatus, UploadedFile, FileState, user_directory_path  # noqa
from code_files.utils import run_flake8
from config.celery import app
from config.settings import MEDIA_ROOT
from users.models import User

logger = logging.getLogger(__name__)


@app.task
def run_flake8_checker():
    """Task for check upload files use flake8."""
    users = User.objects.all()

    for user in users:
        logger.info(f'Work with user: {user}')

        uploaded_files = UploadedFile.objects.filter(
            Q(user=user) & (Q(state=FileState.NEW.value) | Q(state=FileState.OVERWRITTEN.value)),
        )
        logger.debug(f'FILES {type(uploaded_files)} ||| {uploaded_files}')

        for file_ in uploaded_files:
            code_check_obj = CodeCheck.objects.filter(file=file_).first()
            logger.debug(f'FILE {file_} STATUS {code_check_obj.status}')

            if code_check_obj.status == CodeCheckStatus.UNCHECKED.value:
                file_path = Path(MEDIA_ROOT / file_.file.name).resolve()
                logger.info(f'Work with file: {file_path=}')

                code_check_obj.status = CodeCheckStatus.IN_CHECKING.value
                return_code, stdout_, stderr_ = run_flake8(file_path=file_path)

                if stderr_ == '':
                    logger.info(f'RESULT return_code: {return_code}')
                    logger.info(f'RESULT stdout: {stdout_}')
                    code_check_obj.status = CodeCheckStatus.DONE.value
                    file_.state = FileState.OLD.value

                else:
                    logger.info(f'RESULT stderr: {stderr_}')
                    code_check_obj.status = CodeCheckStatus.UNCHECKED.value

                logger.debug(f'END FILE {file_} STATUS {code_check_obj.status}')

                code_check_obj.save()
                file_.save()
            else:
                logger.info(f'No new Files for user: {user}')
