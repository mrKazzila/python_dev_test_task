import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from code_checker.models import CheckLog, CodeCheck
from code_files.models import UploadedFile
from email_sender.email_sender_services import add_info_about_email_send_to_log
from users.models import User


class AddInfoAboutEmailSendToLogTest(TestCase):
    """Test suite for the add_info_about_email_send_to_log function."""

    def setUp(self) -> None:
        """Set up the necessary objects for testing."""
        self.user_instance = User.objects.create_user(email='mrrobot@example.com', password='testpassword')
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user_instance,
            file=SimpleUploadedFile('test_file4.py', b'Test file content'),
            filename='test_file4.py',
        )
        self.code_check = CodeCheck.objects.create(file=self.uploaded_file)

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.uploaded_file.file.delete()
        self.uploaded_file.delete()
        self.user_instance.delete()

    def test_add_info_about_email_send_to_log(self) -> None:
        """Test the add_info_about_email_send_to_log function."""
        add_info_about_email_send_to_log(
            email='mrrobot@example.com',
            code_check_objects_id=[self.code_check.id],
        )

        updated_code_check = CodeCheck.objects.get(pk=self.code_check.id)
        assert updated_code_check.is_notified

        check_log = CheckLog.objects.get(code_check=self.code_check)
        assert check_log.log_text == 'Send email for mrrobot@example.com'

    def test_code_check_not_found(self) -> None:
        """Test handling the case when CodeCheck is not found."""
        with pytest.raises(ObjectDoesNotExist):
            add_info_about_email_send_to_log(
                email='mrrobot@example.com',
                code_check_objects_id=[0],
            )
