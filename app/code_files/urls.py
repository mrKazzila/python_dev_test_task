from django.urls import path
from . import views

app_name = 'code_files'

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('list/', views.file_list, name='file_list'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]
