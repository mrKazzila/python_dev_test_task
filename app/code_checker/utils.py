import subprocess  # nosec B404


def run_flake8(file_path):
    """Run python flake8 module for checking user file."""
    try:
        result = subprocess.run(
            ['flake8', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )  # nosec B603, B607

        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)
