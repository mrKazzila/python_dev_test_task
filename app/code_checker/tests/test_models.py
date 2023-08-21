from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_django.asserts import TestCase

from code_checker.models import CheckLog, CodeCheck, CodeCheckStatus
from code_files.models import UploadedFile
from users.models import User


class BaseSetup(TestCase):

    def setUp(self) -> None:
        """Set up the necessary objects for testing."""
        self.user_instance = User.objects.create_user(email='mrrobot@example.com', password='testpassword')
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user_instance,
            file=SimpleUploadedFile('test_file4.py', b'Test file content'),
        )
        self.code_check = CodeCheck.objects.create(file=self.uploaded_file)

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.uploaded_file.file.delete()
        self.uploaded_file.delete()
        self.user_instance.delete()


class CodeCheckTest(BaseSetup):
    """Test suite for the CodeCheck model."""

    def test_create_code_check(self) -> None:
        """Test creating a CodeCheck instance."""
        assert self.code_check.status == CodeCheckStatus.UNCHECKED.name
        assert self.code_check.last_check_result == 'Without problems'
        assert not self.code_check.is_notified

    def test_delete_code_check(self) -> None:
        """Test deleting a CodeCheck instance and associated CheckLogs."""
        CheckLog.objects.create(code_check=self.code_check, log_text='test')

        self.code_check.delete()

        assert CodeCheck.objects.count() == 0
        assert CheckLog.objects.filter(code_check=self.code_check).count() == 0

    def test_update_code_check_status_to_in_checking(self) -> None:
        """Test updating a CodeCheck status to in checking."""
        self.code_check.status = CodeCheckStatus.IN_CHECKING.name
        assert self.code_check.status == CodeCheckStatus.IN_CHECKING.name

    def test_update_code_check_status_to_done(self) -> None:
        """Test updating a CodeCheck status to done."""
        self.code_check.status = CodeCheckStatus.DONE.name
        assert self.code_check.status == CodeCheckStatus.DONE.name

    def test_update_code_check_last_check_result(self) -> None:
        """Test updating a CodeCheck last_check_result to custom result."""
        result = 'My result'
        self.code_check.last_check_result = result

        assert self.code_check.last_check_result == result

    def test_update_code_check_is_notified(self) -> None:
        """Test updating a CodeCheck is_notified to True."""
        assert not self.code_check.is_notified

        self.code_check.is_notified = True

        assert self.code_check.is_notified


class CheckLogTest(BaseSetup):
    """Test suite for the CheckLog model."""

    def test_check_log_create(self) -> None:
        """Test creating a CheckLog instance."""
        log_text = 'Check log message'
        log = CheckLog.objects.create(code_check=self.code_check, log_text=log_text)

        assert log.log_text == log_text
        assert log.code_check == self.code_check

    def test_check_log_add(self) -> None:
        """Test adding multiple CheckLog instances."""
        CheckLog.objects.create(code_check=self.code_check, log_text='log_text')
        CheckLog.objects.create(code_check=self.code_check, log_text='log_text2')

        assert CheckLog.objects.filter(code_check=self.code_check).count() == 2

    def test_check_log_delete(self) -> None:
        """Test deleting a CheckLog instance."""
        log = CheckLog.objects.create(code_check=self.code_check, log_text='log_text')
        log.delete()

        assert CheckLog.objects.filter(code_check=self.code_check).count() == 0
