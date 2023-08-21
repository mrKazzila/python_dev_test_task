from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve, reverse

from code_files.models import UploadedFile
from reports.views import FileReportView
from users.models import User


class ReportsUrlsTest(TestCase):
    """Test cases for code files URLs."""

    def test_file_report_view_url(self) -> None:
        """Test the URL mapping for the filereport view."""
        user = User.objects.create_user(email='mrrobot2@example.com', password='testpassword')
        file_obj = SimpleUploadedFile('test.py', b'Test file content')
        uploaded_file = UploadedFile.objects.create(user=user, file=file_obj)

        url = reverse('reports:file_report', args=[uploaded_file.id])
        assert resolve(url).func.view_class == FileReportView

        uploaded_file.file.delete()
        user.delete()
