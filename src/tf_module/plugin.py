import logging
import subprocess
from pathlib import Path

import pytest

logger = logging.getLogger("tf-module")


def pytest_configure(config: pytest.Config):
    config.option.log_cli_level = "INFO"


# Fixtures to be overridden


@pytest.fixture(scope="package")
def example_path() -> Path:
    """
    This fixture must be overridden by at the pacakge level and return a path
    to the example under test.
    :return:
    """
    pytest.fail(
        "The example_path fixture must be provided with a path to the example"
        " under test"
    )


# End fixtures to override


class TFExecutionError(Exception):
    pass


def run_terraform_command(command: str, workdir: str | Path | None = None) -> str:
    """
    Run a terraform command with optional extra arguments.
    :param command: The command to run
    :param workdir: The working directory to use
    :return: stdout of the command
    """
    cwd = str(workdir) if workdir else None

    process = subprocess.Popen(
        ["terraform"] + command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        universal_newlines=True,
        cwd=cwd,
    )

    output_lines = []
    while True:
        output = process.stdout.readline() if process.stdout else ""

        if output == "" and process.poll() is not None:
            break
        elif output:
            logger.info(output.strip())
            output_lines.append(output)

    _, err = process.communicate()
    process.wait()

    if process.returncode == 0:
        return "".join(output_lines)
    else:
        logger.error(err)
        raise TFExecutionError("terraform command failed")


@pytest.fixture(scope="package")
def tf_init(example_path: str | Path):
    result = run_terraform_command("init", workdir=example_path)

    return result
