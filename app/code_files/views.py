from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from code_files.forms import FileUploadForm
from code_files.models import UploadedFile


class FileManagementView(LoginRequiredMixin, View):
    template_name = 'code_files/file_list.html'

    def get(self, request):
        if request.user.id is None:
            return redirect('users:signin')

        form = FileUploadForm()
        files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at', '-is_checked', '-is_new')

        paginator = Paginator(files, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj, 'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid() and form.cleaned_data['file'].name.endswith('.py'):
            file_name = str(form.cleaned_data['file'].name)
            owner_id = request.user.id

            is_exist_file = UploadedFile.objects.filter(user=owner_id, filename__exact=file_name).first()

            if is_exist_file:
                new_uploaded_file = form.save(commit=False)
                new_uploaded_file.user = request.user
                new_uploaded_file.is_new = False
                new_uploaded_file.filename = file_name
                new_uploaded_file.is_checked = False
                new_uploaded_file.uploaded_at = datetime.now()
                is_exist_file.delete()
                new_uploaded_file.save()
            else:
                new_uploaded_file = form.save(commit=False)
                new_uploaded_file.user = request.user
                new_uploaded_file.is_new = True
                new_uploaded_file.filename = file_name
                new_uploaded_file.is_checked = False
                new_uploaded_file.save()

            return redirect('code_files:file_list')
        else:
            error_message = 'Only files with the extension .py are allowed'
            form.add_error('file', error_message)

        files = UploadedFile.objects.filter(user=request.user)
        return render(request, self.template_name, {'files': files, 'form': form})


class DeleteFileView(LoginRequiredMixin, View):

    def get(self, request, file_id):
        uploaded_file = UploadedFile.objects.get(pk=file_id)
        if uploaded_file.user == request.user:
            uploaded_file.delete()

        return redirect('code_files:file_list')
