from django import forms

from code_files.models import UploadedFile


class FileUploadForm(forms.ModelForm):
    """Form for uploading files."""

    class Meta:
        model = UploadedFile
        fields = ['file']
