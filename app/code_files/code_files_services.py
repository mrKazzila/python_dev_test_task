from django.core.paginator import Paginator
from django.utils import timezone

from code_checker.models import CodeCheck, CodeCheckStatus
from code_files.models import FileState


def create_files_with_check_status(files):
    """
    Create a list of tuples, each containing a file and its associated CodeCheck object.

    Args:
        files: A QuerySet of UploadedFile objects.

    Returns:
        list: A list of tuples, where each tuple contains an UploadedFile and its associated CodeCheck.
    """
    files_with_checks = []

    for file in files:
        code_check = CodeCheck.objects.filter(file=file).first()
        files_with_checks.append((file, code_check))

    return files_with_checks


def create_paginator_obj(files, page_number):
    """
    Create a paginator object for the given list of files.

    Args:
        files: List of files to be paginated.
        page_number: The page number to retrieve.

    Returns:
        Page: The requested page of files.
    """
    paginator = Paginator(files, 8)

    return paginator.get_page(page_number)


def return_old_file_name_if_file_exist(model, owner, file_name):
    """
    Check if a file with the given name exists for the specified owner in the model.

    Args:
        model: The model to query for file existence.
        owner: ID of the owner user.
        file_name: Name of the file to check.

    Returns:
        True if the file exists, False otherwise.
    """
    existing_file = model.objects.filter(user=owner, filename=file_name).first()

    return existing_file if existing_file else None


def add_new_file(form, user, new_file_name):
    """
    Add a new file entry to the database.

    Args:
        form: The form object containing file data.
        user: The user associated with the file.
        new_file_name: Name of the new file.
    """
    new_file = form.save(commit=False)
    new_file.user = user
    new_file.filename = new_file_name
    new_file.state = FileState.NEW.value

    new_file.save()

    CodeCheck.objects.create(file=new_file, status=CodeCheckStatus.UNCHECKED.value)


def update_exist_file(old_file):
    """
    Update an existing file entry in the database.

    Args:
        old_file: The old file object to update.
    """
    old_file.state = FileState.OVERWRITTEN.value
    old_file.uploaded_at = timezone.now()
    old_file.save()

    CodeCheck.objects.filter(file=old_file).update(status=CodeCheckStatus.UNCHECKED.value)


def delete_file(model, file_pk, user):
    """
    Delete the specified file if it belongs to the given user.

    Args:
        model: The model containing the file to be deleted.
        file_pk: Primary key of the file to be deleted.
        user: The user who owns the file.
    """
    uploaded_file = model.objects.get(pk=file_pk)

    if uploaded_file.user == user:
        uploaded_file.file.delete(save=False)
        uploaded_file.delete()
