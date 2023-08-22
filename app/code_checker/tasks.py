import logging

from code_checker.code_checker_services import (
    check_user_files,
    get_users_files_with_new_or_overwritten_state,
)
from config.celery import app
from email_sender.tasks import send_notification_email

logger = logging.getLogger(__name__)


@app.task(name='Run flake8 checker')
def run_flake8_checker():
    """Task for check upload files use flake8."""
    uploaded_user_files = get_users_files_with_new_or_overwritten_state()

    for user in uploaded_user_files:
        logger.info(f'Work with user: {user}')
        user_uploaded_files = user.filtered_files

        if not user_uploaded_files:
            logger.info(f'No uploaded files for user: {user}')
        else:
            result = check_user_files(uploaded_files=user_uploaded_files)

            send_notification_email.delay(
                user_email=user.email,
                message=result.message,
                code_check_objects_id=result.code_check_objects_id,
            )
