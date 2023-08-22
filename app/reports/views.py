import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from code_checker.models import CodeCheck
from code_files.models import UploadedFile
from common.views import TitleMixin
from reports.reports_services import create_paginator, generate_context, generate_report_info

logger = logging.getLogger(__name__)


class FileReportView(LoginRequiredMixin, TitleMixin, DetailView):
    model = UploadedFile
    title = 'Flake review - Report'
    template_name = 'reports/check_report.html'
    context_object_name = 'file_obj'
    pk_url_kwarg = 'file_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_obj = self.get_object()

        code_checks = CodeCheck.objects.filter(file=file_obj)
        reports = generate_report_info(code_checks=code_checks)

        result_info = create_paginator(
            request=self.request,
            page_count=5,
            obj=reports[0].get('results'),
            prefix='results',
        )
        logs_info = create_paginator(
            request=self.request,
            page_count=2,
            obj=reports[0].get('logs'),
            prefix='logs',
        )

        my_context = generate_context(
            file_obj=file_obj,
            report=reports,
            result_info=result_info,
            logs_info=logs_info,
        )

        context.update(my_context)
        return context
