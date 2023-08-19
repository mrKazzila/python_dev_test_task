from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from code_files.code_files_services import (
    create_files_with_check_status,
    create_paginator_obj,
    delete_file,
    file_manager,
    return_old_file_name_if_file_exist,
)
from code_files.forms import FileUploadForm
from code_files.models import UploadedFile


class FileManagementView(LoginRequiredMixin, View):
    """View for managing user's uploaded files."""

    template_name = 'code_files/file_list.html'

    def get(self, request):
        if request.user.id is None:
            return redirect('users:signin')

        form = FileUploadForm()
        files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at', '-state')

        files_with_checks = create_files_with_check_status(files=files)
        page_obj = create_paginator_obj(files=files_with_checks, page_number=request.GET.get('page'))

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'page_obj': page_obj,
                'form': form,
            },
        )

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid() and form.cleaned_data['file'].name.endswith('.py'):
            file_name = str(form.cleaned_data['file'].name)
            owner_id = request.user.id

            old_file_name = return_old_file_name_if_file_exist(
                model=UploadedFile,
                owner=owner_id,
                file_name=file_name,
            )

            file_manager(
                form=form,
                new_file_name=file_name,
                user=request.user,
                old_file=old_file_name,
            )

            return redirect('code_files:file_list')
        else:
            error_message = 'Only files with the extension .py are allowed'
            form.add_error('file', error_message)

        files = UploadedFile.objects.filter(user=request.user)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'files': files,
                'form': form,
            },
        )


class DeleteFileView(LoginRequiredMixin, View):
    """View for deleting a user's uploaded file."""

    def get(self, request, file_id):
        delete_file(
            model=UploadedFile,
            file_pk=file_id,
            user=request.user,
        )
        return redirect('code_files:file_list')
