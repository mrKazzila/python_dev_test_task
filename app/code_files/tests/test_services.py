from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from code_checker.models import CodeCheck, CodeCheckStatus
from code_files.code_files_services import (
    add_new_file,
    create_files_with_check_status,
    delete_file,
    return_old_file_name_if_file_exist,
    update_exist_file,
)
from code_files.forms import FileUploadForm
from code_files.models import FileState, UploadedFile
from users.models import User


class TestCodeFilesServices(TestCase):
    """Test suite for the code files related services."""

    def setUp(self) -> None:
        """Set up the necessary objects for testing."""
        self.user = User.objects.create_user(email='mrrobot@example.com', password='testpassword')
        self.uploaded_file = SimpleUploadedFile('file.py', b'file_content', content_type='text/plain')
        self.create_file_object = UploadedFile.objects.create(
            user=self.user,
            file=self.uploaded_file,
            filename='file.py',
            state=FileState.NEW.value,
        )

    def tearDown(self) -> None:
        """Clean up after the tests."""
        self.create_file_object.file.delete()
        self.user.delete()

    def test_add_new_file(self) -> None:
        """Test adding a new file using the add_new_file service."""
        form_data = {'file': self.uploaded_file}
        form = FileUploadForm(data={}, files=form_data)
        new_file_name = 'new_file.py'

        add_new_file(form=form, user=self.user, new_file_name=new_file_name)

        file_obj = UploadedFile.objects.filter(user=self.user, filename=new_file_name).first()

        assert UploadedFile.objects.filter(user=self.user, filename=new_file_name).exists()
        assert CodeCheck.objects.filter(file__filename=new_file_name, status=CodeCheckStatus.UNCHECKED.value).exists()

        file_obj.file.delete()

    def test_update_exist_file(self) -> None:
        """Test updating an existing file using the update_exist_file service."""
        old_file = self.create_file_object
        CodeCheck.objects.create(file=old_file, status=CodeCheckStatus.DONE.value)

        old_file.state = FileState.NEW.value
        old_file.uploaded_at = datetime.now()

        update_exist_file(old_file=old_file)

        updated_file = UploadedFile.objects.get(pk=old_file.pk)

        assert updated_file.state == FileState.OVERWRITTEN.value
        assert updated_file.uploaded_at.date() == datetime.now().date()
        assert CodeCheck.objects.filter(file=old_file, status=CodeCheckStatus.UNCHECKED.value).exists()

    def test_delete_file(self) -> None:
        """Test deleting a file using the delete_file service."""
        file_to_delete = self.create_file_object
        file_pk = file_to_delete.pk

        delete_file(model=UploadedFile, file_pk=file_pk, user=self.user)

        assert not UploadedFile.objects.filter(pk=file_pk).exists()

    def test_return_old_file_name_if_file_exist(self) -> None:
        """Test returning the old file name if a file exists using the return_old_file_name_if_file_exist service."""
        old_file = self.create_file_object

        old_file_name = return_old_file_name_if_file_exist(
            model=UploadedFile,
            owner=self.user.id,
            file_name=old_file.filename,
        )

        assert str(old_file_name) == str(old_file)

    def test_return_old_file_name_if_file_not_exist(self) -> None:
        """Test returning None if a file doesn't exist using the return_old_file_name_if_file_exist service."""
        fake_file_name = 'module.py'

        old_file_name = return_old_file_name_if_file_exist(
            model=UploadedFile,
            owner=self.user.id,
            file_name=fake_file_name,
        )

        assert old_file_name is None
        assert old_file_name != fake_file_name

    def test_create_files_with_check_status(self) -> None:
        """Test creating files with associated check statuses using the create_files_with_check_status service."""
        file_obj_1 = UploadedFile.objects.create(
            user=self.user,
            file=SimpleUploadedFile('file3.py', b'file_content', content_type='text/plain'),
            filename='file3.py',
            state=FileState.NEW.value,
        )
        CodeCheck.objects.create(file=file_obj_1, status=CodeCheckStatus.DONE.value)

        file_obj_2 = UploadedFile.objects.create(
            user=self.user,
            file=SimpleUploadedFile('file4.py', b'file_content', content_type='text/plain'),
            filename='file4.py',
            state=FileState.NEW.value,
        )
        CodeCheck.objects.create(file=file_obj_2, status=CodeCheckStatus.UNCHECKED.value)

        files = UploadedFile.objects.filter(user=self.user).order_by('-uploaded_at', '-state')
        files_with_checks = create_files_with_check_status(files=files)

        print(f'TTTSSTS {files_with_checks[:2]}')

        for file_, code_check_ in files_with_checks[:2]:
            assert isinstance(file_, UploadedFile)
            assert isinstance(code_check_, CodeCheck)
            assert code_check_.status in (CodeCheckStatus.UNCHECKED.value, CodeCheckStatus.DONE.value)

        file_obj_1.file.delete()
        file_obj_2.file.delete()
