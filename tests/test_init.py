import pytest


@pytest.fixture
def minimal_tf_config_dir(pytester):
    pytester.makefile(".tf", 'resource "null_resource" "this" {}')


@pytest.fixture
def minimal_test_conftest(pytester):
    conftest = """
    def example():
        return pytester.path
    """
    pytester.makeconftest(conftest)


@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_init_initializes_example_dir(pytester):
    """
    Test that a terraform configuration is initialized by checking for a
    .terraform.lock.hcl.
    """
    test = """
    def test_tf_init(tf_init):
        pass
    """
    pytester.makepyfile(test)
    result = pytester.runpytest()

    result.assert_outcomes(passed=1)
