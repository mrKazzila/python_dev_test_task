import os

import pytest

from code_checker.utils import run_flake8


class RunFlake8Test:
    """Test suite for the run_flake8 utility function."""

    @pytest.mark.parametrize(
        'content, expected_return_code',
        [
            ("print('Hello, world!')\n", 0),
            ("print ('Hello, world!')\n", 1),
        ],
    )
    def test_run_flake8_with_content(self, tmp_path, content, expected_return_code) -> None:
        """Test run_flake8 utility function with content."""
        test_file = tmp_path / 'test_file.py'
        test_file.write_text(content)

        return_code, stdout, stderr = run_flake8(test_file)

        assert return_code == expected_return_code

        if expected_return_code == 0:
            assert stdout == ''
            assert stderr == ''
        else:
            assert 'E211' in stdout

        os.remove(test_file)

    def test_run_flake8_with_non_existent_file(self, tmp_path) -> None:
        """Test run_flake8 utility function with a non-existent file."""
        non_existent_file = tmp_path / 'non_existent_file.py'

        return_code, stdout, stderr = run_flake8(non_existent_file)

        assert return_code == 1
        assert 'No such file or directory' in stdout
        assert stderr == ''
