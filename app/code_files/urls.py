from django.urls import path

from .views import DeleteFileView, FileManagementView

app_name = 'code_files'

urlpatterns = [
    path('list/', FileManagementView.as_view(), name='file_list'),
    path('delete/<int:file_id>/', DeleteFileView.as_view(), name='delete_file'),
]
