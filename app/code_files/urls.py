from django.urls import path

from .views import FileManagementView, delete_file

app_name = 'code_files'

urlpatterns = [
    path('list/', FileManagementView.as_view(), name='file_list'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]
