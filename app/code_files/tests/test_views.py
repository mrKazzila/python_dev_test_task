import tempfile

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from code_files.models import UploadedFile
from users.models import User


class BaseSetUp(TestCase):

    def setUp(self) -> None:
        """Set up the necessary objects for testing."""
        self.user = User.objects.create_user(email='mrrobot2@example.com', password='testpassword')
        self.client = Client()
        file_obj = SimpleUploadedFile('test.py', b'Test file content')
        self.uploaded_file = UploadedFile.objects.create(user=self.user, file=file_obj)

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.uploaded_file.file.delete()
        self.user.delete()


class TestFileManagementView(BaseSetUp):
    """Test cases for the FileManagementView."""

    def test_get_with_login(self) -> None:
        """Test the GET request to the file management view with a logged-in user."""
        url = reverse('code_files:file_list')
        self.client.login(email='mrrobot2@example.com', password='testpassword')

        response = self.client.get(url)

        assert response.status_code == 200
        assert 'code_files/file_list.html' in [t.name for t in response.templates]

    def test_get_without_login(self) -> None:
        """Test the GET request to the file management view without being logged in."""
        url = reverse('code_files:file_list')

        response = self.client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('users:signin') + '?next=' + reverse('code_files:file_list')

    def test_post_upload_valid_py_file(self) -> None:
        """Test uploading a valid .py file using the POST request to the file management view."""
        url = reverse('code_files:file_list')
        self.client.login(email='mrrobot2@example.com', password='testpassword')

        tmp_file_name = 'test_tmp.py'

        with tempfile.NamedTemporaryFile(prefix=tmp_file_name, suffix='.py', delete=True) as temp_file:
            temp_file.write(b"print('Hello, World!')\n")
            temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as file:
                response = self.client.post(url, {'file': file})

        assert response.status_code == 200
        file_ = UploadedFile.objects.filter(user=self.user).last()

        assert file_ is not None
        assert file_.file.name.endswith('.py')

        file_.file.delete()

    def test_post_upload_invalid_file_format(self) -> None:
        """Test uploading a file with an invalid format using the POST request to the file management view."""
        url = reverse('code_files:file_list')
        self.client.login(email='mrrobot2@example.com', password='testpassword')

        tmp_file_name = 'test_tmp.txt'

        with tempfile.NamedTemporaryFile(prefix=tmp_file_name, suffix='.txt', delete=True) as temp_file:
            temp_file.write(b"print('Hello, World!')\n")
            temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as file:
                response = self.client.post(url, {'file': file})

        assert response.status_code == 200
        assert b'Only files with the extension .py are allowed' in response.content

        uploaded_file = UploadedFile.objects.filter(user=self.user).all()
        assert tmp_file_name not in uploaded_file

    def test_post_upload_file_without_login(self) -> None:
        """Test uploading a file without being logged in using the POST request to the file management view."""
        url = reverse('code_files:file_list')

        tmp_file_name = 'test_tmp.py'

        with tempfile.NamedTemporaryFile(prefix=tmp_file_name, suffix='.py', delete=True) as temp_file:
            temp_file.write(b"print('Hello, World!')\n")
            temp_file_path = temp_file.name

            with open(temp_file_path, 'rb') as file:
                response = self.client.post(url, {'file': file})

        assert response.status_code == 302
        assert response.url == reverse('users:signin') + '?next=' + reverse('code_files:file_list')


class TestDeleteFileView(BaseSetUp):
    """Test cases for the DeleteFileView."""

    def test_get_delete_file(self) -> None:
        """Test the GET request to delete a file."""
        self.client.login(email='mrrobot2@example.com', password='testpassword')

        url = reverse('code_files:delete_file', args=[self.uploaded_file.id])
        response = self.client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('code_files:file_list')
        with pytest.raises(ObjectDoesNotExist):
            UploadedFile.objects.get(file=self.uploaded_file)
