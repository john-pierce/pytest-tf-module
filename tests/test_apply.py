import pytest


@pytest.mark.xfail(strict=True)
@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_apply_applies_configuration(pytester):
    """ "
    Test that requesting the tf_apply fixture causes a sample configuration to
    be applied by checking:
      - pytest returns a successful result
      - Terraform output displays that the apply has been successful
      - a terraform.tfstate file exists
    """

    test = """
    def test_tf_apply(tf_apply):
        pass
    """
    pytester.makepyfile(test)
    result = pytester.runpytest_subprocess()

    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(["pytest-tf-module FAIL"])

    assert (pytester.path / "terraform.tfstate").exists() is True


@pytest.mark.xfail(strict=True)
@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_apply_initializes_first(pytester):
    test = """
    def test_tf_apply(tf_apply):
        pass
    """
    pytester.makepyfile(test)
    result = pytester.runpytest_subprocess()

    result.stdout.fnmatch_lines(["*Terraform has been successfully initialized!*"])
