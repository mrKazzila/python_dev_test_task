import re
from unittest.mock import Mock, patch

import pytest
from django.core.paginator import Paginator

from reports.reports_services import (
    create_paginator,
    extract_error_components,
    generate_context,
    generate_report_info,
    generate_result_report,
    parse_row_result,
)


@pytest.fixture
def mock_code_check():
    mock_check = Mock()
    mock_check.timestamp = '2023-08-21 12:00:00'
    mock_check.status = 'Passed'
    mock_check.is_notified = True
    mock_check.last_check_result = 'Without problems'
    return mock_check


@pytest.fixture
def mock_check_log():
    mock_log = Mock()
    mock_log.created_at = '2023-08-21 12:00:00'
    return mock_log


class ReportServicesTest:

    @patch('code_checker.models.CheckLog.objects.filter')
    def test_generate_report_info(self, mock_filter, mock_code_check, mock_check_log) -> None:
        """Test generating a report with mock data."""
        mock_code_checks = [mock_code_check]
        mock_filter.return_value.order_by.return_value = [mock_check_log]

        report = generate_report_info(code_checks=mock_code_checks)

        assert len(report) == 1
        assert report[0]['check_date'] == mock_code_check.timestamp
        assert report[0]['status'] == mock_code_check.status
        assert report[0]['is_notified'] == mock_code_check.is_notified
        assert report[0]['results'][0].error_text == 'Without problems'
        assert report[0]['logs'][0] == mock_check_log

    def test_generate_result_report(self) -> None:
        """Test generating a result report."""
        row = 'Without problems'

        report = generate_result_report(row_result=row)

        assert len(report) == 1
        assert report[0].error_text == 'Without problems'

    def test_parse_row_result(self) -> None:
        """Test parsing a row result into lines."""
        row = 'Line 1\nLine 2\nLine 3'

        lines = parse_row_result(row_result=row)

        assert len(lines) == 3
        assert lines[0] == 'Line 1'
        assert lines[1] == 'Line 2'
        assert lines[2] == 'Line 3'

    def test_extract_error_components(self) -> None:
        """Test extracting error components from a line."""
        line = 'file.py:10:5: E123 some error text'
        location_match_pattern = re.compile(r'^([^:]+:\d+:\d+):')
        error_code_match_pattern = re.compile(r'^.*:\d+:\d+:\s*([A-Z]\d+)\s')
        error_text_match_pattern = re.compile(r'^.*:\d+:\d+:\s*[A-Z]\d+\s(.+)')

        location, error_code, error_text = extract_error_components(
            line=line,
            location_regex=location_match_pattern,
            error_code_regex=error_code_match_pattern,
            error_text_regex=error_text_match_pattern,
        )

        assert location == 'file.py:10:5'
        assert error_code == 'E123'
        assert error_text == 'some error text'

    def test_create_paginator(self) -> None:
        """Test creating a paginator for an object."""
        request = Mock()
        request.GET = {'prefix_page': 2}
        page_count = 10
        obj = [1, 2, 3, 4, 5]
        prefix = 'prefix'

        paginator = create_paginator(
            request=request,
            page_count=page_count,
            obj=obj,
            prefix=prefix,
        )

        assert isinstance(paginator.paginator, Paginator)
        assert paginator.paginator.num_pages == 1
        assert paginator.paginator.count == 5
        assert paginator.paginator.page(1).object_list == [1, 2, 3, 4, 5]

    def test_generate_context(self) -> None:
        """Test generating a context dictionary."""
        file_obj = Mock()
        report = [{'error_text': 'Error 1'}, {'error_text': 'Error 2'}]
        result_info = Mock()
        logs_info = Mock()

        context = generate_context(
            file_obj=file_obj,
            report=report,
            result_info=result_info,
            logs_info=logs_info,
        )

        assert context['file_obj'] == file_obj
        assert context['report'] == report
        assert context['result_info'] == result_info
        assert context['logs_info'] == logs_info
