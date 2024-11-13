import pytest


@pytest.fixture
def minimal_tf_config_dir(pytester):
    pytester.makefile(".tf", 'resource "null_resource" "this" {}')


@pytest.fixture
def minimal_test_conftest(pytester):
    conftest = """
    import pytest
    
    @pytest.fixture(scope="package")
    def example_path():
        return "{pytester_path}"
    """.format(pytester_path=pytester.path)

    pytester.makeconftest(conftest)


@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_init_initializes_example_dir(pytester):
    """
    Test that a terraform configuration is initialized by checking:
      - A .terraform.lock.hcl file exists
      - Terraform output is displayed
      - Terraform returns a successful exit code
    """
    test = """
    def test_tf_init(tf_init):
        pass
    """
    pytester.makepyfile(test)
    result = pytester.runpytest_subprocess()

    result.assert_outcomes(passed=1)

    assert (pytester.path / ".terraform.lock.hcl").exists() is True

    result.stdout.fnmatch_lines(["*Terraform has been successfully initialized!*"])


def test_tf_fails_if_example_path_is_unset(pytester):
    test = """
    def test_should_fail(tf_init):
        pass
    """

    pytester.makepyfile(test)
    result = pytester.runpytest_subprocess()

    result.assert_outcomes(errors=1)

    result.stdout.fnmatch_lines(["*example_path*"])
