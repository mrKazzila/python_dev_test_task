from django.conf import settings
from django.core.mail import send_mail

from config.celery import app
from email_sender.email_sender_services import add_info_about_email_send_to_log


@app.task(name='Send notification email')
def send_notification_email(user_email, message, code_check_objects_id):
    send_mail(
        subject='The result of checking your file.',
        message=f'Dear {user_email}!\n\n{message}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )

    add_info_about_email_send_to_log(email=user_email, code_check_objects_id=code_check_objects_id)
