import textwrap

import pytest


@pytest.mark.usefixtures("outputs_tf")
def test_tf_output_returns_outputs_as_dictionary(
    pytester, sample_skeleton, example_name
):
    tests_path = sample_skeleton / "tests" / example_name / "test_output_1.py"
    with tests_path.open("w") as f:
        test_content = """
        def test_output(tf_output):
            assert tf_output["static"] == "static output"
        """
        f.write(textwrap.dedent(test_content))

    result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)


@pytest.fixture
def outputs_tf(pytester, sample_skeleton, example_name):
    outputs_tf_path = sample_skeleton / "examples" / example_name / "outputs.tf"
    with outputs_tf_path.open("w") as f:
        outputs_tf_content = """
        output "static" {
            value = "static output"
        }
        """
        f.write(textwrap.dedent(outputs_tf_content))

    return outputs_tf_path


pytest_plugins = ["pytester"]
