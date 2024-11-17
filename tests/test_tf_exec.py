import pytest

from tf_module.plugin import TFExecutionError, run_terraform_command


def test_tf_exec_falure_should_raise_TFExecutionError_on_failure():
    with pytest.raises(TFExecutionError):
        run_terraform_command("no-such-command")
