from django.urls import path
from reports.views import FileReportView

app_name = 'reports'

urlpatterns = [
    path('file/<int:file_id>/', FileReportView.as_view(), name='file_report'),
]
