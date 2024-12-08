import pytest

from tf_module.plugin import TFExecutionError, run_terraform_command


def test_tf_exec_falure_should_raise_TFExecutionError_on_failure():
    with pytest.raises(TFExecutionError):
        run_terraform_command("no-such-command")


@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_exec_should_log_invocation_parameters(pytester):
    test_content = """
    import pytest
    @pytest.fixture(scope="package")
    def tf_variables():
        return {"pytest_var": "pytest_value"}
    def test_apply(tf_apply):
        pass
    """
    pytester.makepyfile(test_content)

    conftest_tf = """
    variable "pytest_var" {}
    """
    pytester.makefile(".tf", conftest_tf)

    result = pytester.runpytest_subprocess()

    result.stdout.re_match_lines(
        [r".*Running 'terraform apply.* -var pytest_var=pytest_value('|\s.*')$"]
    )


pytest_plugins = ["pytester"]
