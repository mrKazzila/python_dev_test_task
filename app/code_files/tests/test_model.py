from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_django.asserts import TestCase

from code_files.models import FileState, UploadedFile
from users.models import User


class TestUploadedFile(TestCase):
    """Test suite for the UploadedFile model."""

    def setUp(self) -> None:
        """Set up the necessary objects for testing."""
        self.user_instance = User.objects.create_user(email='mrrobot@example.com', password='testpassword')
        self.user_id = self.user_instance.id
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user_instance,
            file=SimpleUploadedFile('test_file4.py', b'Test file content'),
        )

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.uploaded_file.file.delete()
        self.uploaded_file.delete()

    def test_file_creation(self) -> None:
        """Test if an UploadedFile instance is created correctly."""
        assert str(self.uploaded_file) == f'user_{self.user_id}/code/test_file4.py'
        assert self.uploaded_file.state == FileState.NEW.value

    def test_str_method(self) -> None:
        """Test the __str__ method of the UploadedFile model."""
        assert str(self.uploaded_file) == f'user_{self.user_id}/code/test_file4.py'

    def test_default_state(self) -> None:
        """Test the default state of a newly created UploadedFile."""
        assert self.uploaded_file.state == FileState.NEW.value

    def test_state_change_to_overwritten(self) -> None:
        """Test changing the state of an UploadedFile to OVERWRITTEN."""
        self.uploaded_file.state = FileState.OVERWRITTEN.value
        self.uploaded_file.save()

        assert self.uploaded_file.state == FileState.OVERWRITTEN.value

    def test_state_change_to_old(self) -> None:
        """Test changing the state of an UploadedFile to OLD."""
        self.uploaded_file.state = FileState.OLD.value
        self.uploaded_file.save()

        assert self.uploaded_file.state == FileState.OLD.value
