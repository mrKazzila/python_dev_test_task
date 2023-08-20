from code_checker.models import CheckLog, CodeCheck


def add_info_about_email_send_to_log(email, code_check_objects_id):
    for code_check_id in code_check_objects_id:
        code_check = CodeCheck.objects.get(pk=code_check_id)

        code_check.is_notified = True
        code_check.save()

        CheckLog.objects.create(code_check=code_check, log_text=f'Send email for {email}')
