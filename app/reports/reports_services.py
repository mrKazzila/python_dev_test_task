import logging
import re
from collections import namedtuple

from django.core.paginator import Paginator

from code_checker.models import CheckLog

logger = logging.getLogger(__name__)


def generate_report_info(code_checks):
    """
    Generate a report information list from a list of CodeCheck.

    Args:
        code_checks: A list of CodeCheck objects.

    Returns:
        A list of dictionaries containing check date, status, notification status, result report, and related logs.
    """
    report = []

    for check in code_checks:
        report_message = generate_result_report(row_result=check.last_check_result)

        report.append(
            {
                'check_date': check.timestamp,
                'status': check.status,
                'is_notified': check.is_notified,
                'results': report_message,
                'logs': CheckLog.objects.filter(code_check=check).order_by('-created_at'),
            },
        )

    return report


def generate_result_report(row_result):
    """
    Generate a report from a row result string.

    Args:
        row_result: The row result string to generate a report from.

    Returns:
        A list of namedtuples containing location, error code, and error text.
    """
    if row_result == 'Without problems':
        return [create_file_report(location='-', error_code='-', error_text='Without problems')]

    pattern = re.compile(r'^\/home\/unprivilegeduser\/code\/app\/media\/user_\d+\/code\/', flags=re.MULTILINE)
    location_match_pattern = re.compile(r'^([^:]+:\d+:\d+):')
    error_code_match_pattern = re.compile(r'^.*:\d+:\d+:\s*([A-Z]\d+)\s')
    error_text_match_pattern = re.compile(r'^.*:\d+:\d+:\s*[A-Z]\d+\s(.+)')

    result = pattern.sub('', row_result)
    lines = parse_row_result(result)

    report_result = []

    for line in lines:
        location, error_code, error_text = extract_error_components(
            line=line,
            location_regex=location_match_pattern,
            error_code_regex=error_code_match_pattern,
            error_text_regex=error_text_match_pattern,
        )

        rep = create_file_report(location=location, error_code=error_code, error_text=error_text)
        report_result.append(rep)

    return report_result


def create_file_report(location, error_code, error_text):
    """
    Create a named tuple representing a file report.

    Args:
        location: Location of the error.
        error_code: Error code.
        error_text: Error text.

    Returns:
        A named tuple representing a file report.
    """
    return namedtuple('FileReport', 'location, error_code, error_text')(location, error_code, error_text)


def parse_row_result(row_result):
    """
    Parse a row result string into lines.

    Args:
        row_result: The row result string to parse.

    Returns:
        A list of lines from the row result.
    """
    return row_result.strip().split('\n')


def extract_error_components(line, location_regex, error_code_regex, error_text_regex):
    """
    Extract error components from a line.

    Args:
        line: The line to extract error components from.
        location_regex: Regex pattern for location.
        error_code_regex: Regex pattern for error code.
        error_text_regex: Regex pattern for error text.

    Returns:
        A tuple containing location, error code, and error text extracted from the line.
    """
    location_match = location_regex.match(line)
    error_code_match = error_code_regex.match(line)
    error_text_match = error_text_regex.match(line)

    location = location_match.group(1) if location_match else ''
    error_code = error_code_match.group(1) if error_code_match else ''
    error_text = error_text_match.group(1) if error_text_match else ''

    return location, error_code, error_text


def create_paginator(request, page_count, obj, prefix):
    """
    Create a paginator for a given object based on the request's query parameters.

    Args:
        request: The HTTP request object.
        page_count: The number of items per page.
        obj: The iterable object to paginate.
        prefix: The prefix for the page query parameter.

    Returns:
        A Page object containing the paginated items.
    """
    paginator = Paginator(obj, page_count)
    page_number = request.GET.get(f'{prefix}_page')

    return paginator.get_page(page_number)


def generate_context(file_obj, report, result_info, logs_info):
    """
    Generate a context dictionary for rendering in templates.

    Args:
        file_obj: The file object.
        report: The report information.
        result_info: Paginator result information.
        logs_info: Information about logs with paginator.

    Returns:
        A dictionary containing the context information.
    """
    return dict(file_obj=file_obj, report=report, result_info=result_info, logs_info=logs_info)
