from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve, reverse

from code_files.models import UploadedFile
from code_files.views import DeleteFileView, FileManagementView
from users.models import User


class CodeFilesUrlsTest(TestCase):
    """Test cases for code files URLs."""

    def test_file_management_view_url(self) -> None:
        """Test the URL mapping for the file management view."""
        url = reverse('code_files:file_list')
        assert resolve(url).func.view_class == FileManagementView

    def test_delete_file_view_url(self) -> None:
        """Test the URL mapping for the delete file view."""
        user = User.objects.create_user(email='mrrobot2@example.com', password='testpassword')
        file_obj = SimpleUploadedFile('test.py', b'Test file content')
        uploaded_file = UploadedFile.objects.create(user=user, file=file_obj)

        url = reverse('code_files:delete_file', args=[uploaded_file.id])
        assert resolve(url).func.view_class == DeleteFileView

        uploaded_file.file.delete()
        user.delete()
