import logging

from code_checker.code_checker_services import (
    check_user_files,
    get_new_or_overwritten_user_files,
)
from code_files.models import UploadedFile
from config.celery import app
from email_sender.tasks import send_notification_email
from users.models import User

logger = logging.getLogger(__name__)


@app.task(name='Run flake8 checker')
def run_flake8_checker():
    """Task for check upload files use flake8."""
    users = User.objects.all()

    for user in users:
        logger.debug(f'Work with user: {user}')
        uploaded_files = get_new_or_overwritten_user_files(upload_file_model=UploadedFile, user=user)

        if not uploaded_files:
            logger.debug(f'No new Files for user: {user}')
        else:
            files_checking_log, code_checker_objects = check_user_files(uploaded_files=uploaded_files)

            send_notification_email.delay(
                user_email=user.email,
                message=files_checking_log,
                code_check_objects_id=code_checker_objects,
            )
