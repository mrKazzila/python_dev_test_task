from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import UploadedFile, user_directory_path


@login_required
def upload_file(request):
    print(request.method)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        print(f'{form}')
        print(f'{form.files}')

        file_name = str(form.cleaned_data['file'].name)
        print(f'{file_name}')

        if form.is_valid() and file_name.endswith('.py'):
            owner_id = request.user.id
            file_path = user_directory_path(request, file_name)

            is_exist_file = UploadedFile.objects.filter(user=owner_id, file__exact=file_path).first()

            if is_exist_file:
                is_exist_file.file = file_name
                is_exist_file.is_new = False
                is_exist_file.save()
            else:
                new_uploaded_file = form.save(commit=False)
                new_uploaded_file.user = request.user
                new_uploaded_file.is_new = True
                new_uploaded_file.filename = file_name
                new_uploaded_file.save()

            return redirect('code_files:file_list')
        else:
            error_message = 'Only files with the extension are allowed .py'
            form.add_error('file', error_message)
    else:
        form = FileUploadForm()

    return render(request, 'code_files/upload.html', {'form': form})


def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    print(files)
    return render(request, 'code_files/file_list.html', {'files': files})


@login_required
def delete_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    if uploaded_file.user == request.user:
        uploaded_file.delete()

    return redirect('code_files:file_list')
