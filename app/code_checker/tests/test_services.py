from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from code_checker.code_checker_services import (
    _generate_message_for_email,
    _generate_path_to_user_file,
    _generate_str_with_checked_files,
    get_users_files_with_new_or_overwritten_state,
)
from code_checker.models import CodeCheck
from code_checker.utils import run_flake8
from code_files.models import FileState
from code_files.models import UploadedFile
from users.models import User


class TestCodeCheckerServices(TestCase):

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

    @patch('code_checker.utils.subprocess.run')
    def test_run_flake8(self, mock_subprocess_run) -> None:
        """Test for run_flake8 function from utils."""
        mock_subprocess_run.return_value = Mock(returncode=0, stdout='', stderr='')

        return_code, stdout, stderr = run_flake8('path/to/file.py')

        assert return_code == 0
        assert stdout == ''
        assert stderr == ''

    def test_get_users_files_with_new_or_overwritten_state(self) -> None:
        """Test get_users_files_with_new_or_overwritten_state function return only NEW and OVERWRITTEN files."""
        uploaded_file1 = UploadedFile.objects.create(
            file=SimpleUploadedFile('test_file1.py', b'Test file content'),
            user=self.user_instance,
            state=FileState.NEW.value,
        )
        uploaded_file2 = UploadedFile.objects.create(
            file=SimpleUploadedFile('test_file2.py', b'Test file2 content'),
            user=self.user_instance,
            state=FileState.OVERWRITTEN.value,
        )
        uploaded_file3 = UploadedFile.objects.create(
            file=SimpleUploadedFile('test_file3.py', b'Test file2 content'),
            user=self.user_instance,
            state=FileState.OLD.value,
        )

        users_with_files = get_users_files_with_new_or_overwritten_state()
        assert users_with_files.count() == 1

        get_user_with_files = users_with_files[0]

        assert get_user_with_files.email == self.user_instance.email

        assert uploaded_file1 in get_user_with_files.filtered_files
        assert uploaded_file2 in get_user_with_files.filtered_files
        assert uploaded_file3 not in get_user_with_files.filtered_files

        uploaded_file1.file.delete()
        uploaded_file2.file.delete()
        uploaded_file3.file.delete()

    def test_generate_path_to_user_file(self) -> None:
        """Test for _generate_path_to_user_file function."""
        absolute_file_path, file_name = _generate_path_to_user_file(self.uploaded_file)

        assert isinstance(absolute_file_path, Path)
        assert file_name == 'test_file4.py'


def test_generate_message_for_email() -> None:
    """Test for _generate_message_for_email function."""
    files = ['test_file1.py', 'test_file2.py']
    message = _generate_message_for_email(files)

    assert message.startswith('We checked your code')


@pytest.mark.parametrize(
    'files, expected_result',
    [
        (['test_file1.py', 'test_file2.py'], 'files: test_file1.py, test_file2.py.'),
        (['test_file1.py'], 'file test_file1.py.'),
    ],
)
def test_generate_str_with_checked_files(files, expected_result) -> None:
    """Test for _generate_str_with_checked_files function."""
    result = _generate_str_with_checked_files(files)

    assert result == expected_result
