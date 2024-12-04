import textwrap

import pytest


@pytest.mark.usefixtures("variables_tf")
def test_tf_variables_are_passed_to_terraform(pytester, sample_skeleton, example_name):
    tests_path = sample_skeleton / "tests" / example_name / "test_variables_1.py"
    with tests_path.open("w") as f:
        test_content = """
        import pytest

        @pytest.fixture(scope="package")
        def tf_variables():
            return {"passthrough": "pytest" }

        def test_output(tf_output):
            assert tf_output["passthrough"] == "pytest" 
        """
        f.write(textwrap.dedent(test_content))

    result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)


@pytest.mark.usefixtures("variables_tf")
def test_tf_variables_can_be_passed_dictionaries(
    pytester, sample_skeleton, example_name
):
    tests_path = sample_skeleton / "tests" / example_name / "test_variables_1.py"
    with tests_path.open("w") as f:
        test_content = """
        import pytest

        @pytest.fixture(scope="package")
        def tf_variables():
            return {"passthrough_map": {"key": "value"}}

        def test_output(tf_output):
            assert tf_output["passthrough_map"] == {"key": "value"}
        """
        f.write(textwrap.dedent(test_content))

    result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)


@pytest.mark.usefixtures("variables_tf")
def test_tf_variables_can_be_passed_lists(pytester, sample_skeleton, example_name):
    tests_path = sample_skeleton / "tests" / example_name / "test_variables_1.py"
    with tests_path.open("w") as f:
        test_content = """
        import pytest

        @pytest.fixture(scope="package")
        def tf_variables():
            return {"passthrough_list": ["a", 1, "b"]}

        def test_output(tf_output):
            # Terraform outputs all elements of a list as strings, even
            # numerical values.
            assert tf_output["passthrough_list"] == ["a", "1", "b"]
        """
        f.write(textwrap.dedent(test_content))

    result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)


@pytest.fixture
def variables_tf(pytester, sample_skeleton, example_name):
    variables_tf_path = sample_skeleton / "examples" / example_name / "variables.tf"
    with variables_tf_path.open("w") as f:
        variables_content = """
        variable "passthrough" { default = null }
        variable "passthrough_map" {
            type = map
            default = null
        }
        variable "passthrough_list" {
            type = list
            default = null
        }
        output "passthrough" { value = var.passthrough }
        output "passthrough_map" { value = var.passthrough_map }
        output "passthrough_list" { value = var.passthrough_list }
        """
        f.write(textwrap.dedent(variables_content))

    return variables_tf_path


pytest_plugins = ["pytester"]
