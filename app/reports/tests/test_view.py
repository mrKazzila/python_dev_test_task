from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from code_checker.models import CodeCheck, CodeCheckStatus
from code_files.models import UploadedFile
from users.models import User


class TestFileReportView(TestCase):

    def setUp(self) -> None:
        """Set up the client for testing."""
        self.user = User.objects.create_user(email='mrrobor@gmail.com', password='testpassword')
        self.client = Client()
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user,
            file=SimpleUploadedFile('test_file.py', b'Test file content'),
            filename='test_file.py',
        )
        self.code_check = CodeCheck.objects.create(
            file=self.uploaded_file,
            status=CodeCheckStatus.UNCHECKED.value,
            last_check_result='Without problems',
        )

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.uploaded_file.file.delete()
        self.uploaded_file.delete()
        self.user.delete()

    def test_view_requires_login(self) -> None:
        """Test that the view requires login and redirects if not logged in."""
        response = self.client.get(reverse('reports:file_report', kwargs={'file_id': 1}))

        assert response.status_code == 302
        assert response.url.startswith('/users/signin/')

    def test_view_render_correct_template(self) -> None:
        """Test that the view renders the correct template for authenticated users."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('reports:file_report', kwargs={'file_id': self.uploaded_file.pk}))

        assert response.status_code == 200
        assert 'reports/check_report.html' in response.template_name

    def test_context_data(self) -> None:
        """Test that the context contains the expected data."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('reports:file_report', kwargs={'file_id': self.uploaded_file.pk}))

        assert response.status_code == 200
        assert 'file_obj' in response.context
        assert 'report' in response.context
        assert 'result_info' in response.context
        assert 'logs_info' in response.context

    def test_report_and_pagination(self) -> None:
        """Test that the report and pagination work as expected."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('reports:file_report', kwargs={'file_id': self.uploaded_file.pk}))

        assert response.status_code == 200
        report = response.context['report']
        result_info = response.context['result_info']
        logs_info = response.context['logs_info']

        assert len(report) == 1
        assert len(result_info) == 1
        assert len(logs_info) == 0
