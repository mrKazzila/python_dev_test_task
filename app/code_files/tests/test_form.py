from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from code_files.forms import FileUploadForm
from code_files.models import FileState
from users.models import User


class TestFileUploadForm(TestCase):
    """Test suite for the FileUploadForm class."""

    def setUp(self) -> None:
        """Set up a user instance for testing."""
        self.user_instance = User.objects.create_user(email='mrrobot@example.com', password='testpassword')

    def tearDown(self) -> None:
        self.user_instance.delete()

    def test_valid_form(self) -> None:
        """Test if the form is valid when all required data is provided."""
        file_data = {'file': SimpleUploadedFile('test_file.py', b'file_content')}
        form = FileUploadForm(data={}, files=file_data)
        form.instance.user = self.user_instance

        assert form.is_valid()

    def test_invalid_form_missing_file(self) -> None:
        """Test if the form is invalid when the 'file' field is missing."""
        form = FileUploadForm(data={})
        form.instance.user = self.user_instance

        assert not form.is_valid()
        assert 'file' in form.errors

    def test_user_directory_path(self) -> None:
        """Test if the uploaded file is saved with the correct path and state."""
        filename = 'test_file2.py'
        file_data = {'file': SimpleUploadedFile(filename, b'file_content')}

        form = FileUploadForm(data={}, files=file_data)
        form.instance.user = self.user_instance

        assert form.is_valid()

        uploaded_file = form.save()
        expected_path = f'user_{self.user_instance.id}/code/{filename}'

        assert uploaded_file.file.name == expected_path
        assert uploaded_file.state == FileState.NEW.value

        uploaded_file.file.delete()
