import json
import logging
import os
import subprocess
from collections.abc import Generator
from pathlib import Path
from typing import List, Union

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

JSONType = Union[str, int, float, bool, None, dict[str, "JSONType"], list["JSONType"]]


class TFExecutionError(Exception):
    pass


def run_terraform_command(
    command: str, workdir: str | Path | None = None, tf_args: list[str] | None = None
) -> str:
    """
    Run a terraform command with optional extra arguments.
    :param command: The command to run
    :param workdir: The working directory to use
    :return: stdout of the command
    """
    cwd = str(workdir) if workdir else None

    run_env = os.environ.copy()
    if "TF_INPUT" not in os.environ:
        run_env["TF_INPUT"] = "0"

    run_env["TF_IN_AUTOMATION"] = "1"

    cmd_args = tf_args or []

    process = subprocess.Popen(
        ["terraform"] + command.split() + cmd_args,
        env=run_env,
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
def tf_init(example_path: str | Path) -> str:
    result = run_terraform_command("init", workdir=example_path)

    return result


@pytest.fixture(scope="package")
def tf_apply(
    tf_init: str, tf_destroy: None, example_path: str | Path, tf_var_args: List[str]
) -> str:
    result = run_terraform_command(
        "apply", tf_args=["-auto-approve"] + tf_var_args, workdir=example_path
    )

    return result


@pytest.fixture(scope="package")
def tf_destroy(
    example_path: str | Path, tf_var_args: List[str]
) -> Generator[None, None, None]:
    """
    Calls terraform destroy on teardown after tests are finished.

    Because the command runs during teardown, there's nothing to return.

    terraform output is still logged.
    """
    yield

    run_terraform_command(
        "destroy", tf_args=["-auto-approve"] + tf_var_args, workdir=example_path
    )


@pytest.fixture(scope="package")
def tf_output(tf_apply, example_path: str | Path) -> JSONType:
    result = run_terraform_command("output", tf_args=["-json"], workdir=example_path)

    outputs = json.loads(result)
    return {k: v["value"] for k, v in outputs.items()}


@pytest.fixture(scope="package")
def tf_variables():
    return {}


@pytest.fixture(scope="package")
def tf_var_args(tf_variables):
    args = []
    for k, v in tf_variables.items():
        match v:
            case dict() | list():
                value = json.dumps(v)
            case _:
                value = str(v)

        args += ["-var", f"{k}={value}"]

    return args
