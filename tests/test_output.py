import pytest


@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_output_returns_outputs_as_dictionary(pytester):
    outputs_tf_content = """
    output "null_resource" {
        value = null_resource.this
    }
    """
    pytester.makefile(".tf", outputs_tf_content)

    test_content = """
    def test_output(tf_output):
        assert tf_output["null_resource"] == {}
    """
    pytester.makepyfile(test_content)

    result = pytester.runpytest_subprocess()

    result.assert_outcomes(passed=1)


pytest_plugins = ["pytester"]
