import textwrap

import pytest


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


@pytest.mark.usefixtures("sample_conftest", "tf_init_test")
def test_tf_example_path_can_be_relative_to_project_root_or_absolute(
    pytester, example_name
):
    result = pytester.runpytest_subprocess()
    result.assert_outcomes(passed=1)

    result.stdout.no_fnmatch_line("*empty directory!*")

    result.stdout.fnmatch_lines(
        [
            "*has been successfully initialized*",
        ]
    )


@pytest.fixture(
    params=[
        "pathlib.Path('.')",
        "pytestconfig.rootpath",
    ],
    ids=["relative", "absolute"],
)
def sample_conftest(request, sample_skeleton, example_name):
    """
    Crate example test conftest.py with an absolute or relative path.
    """
    conftest_py_content = f"""
    import pathlib, pytest
    @pytest.fixture(scope="package")
    def example_path(pytestconfig):
        return {request.param} / "examples" / "{example_name}"
    """
    conftest_py_path = sample_skeleton / "tests" / example_name / "conftest.py"
    with conftest_py_path.open("w") as f:
        f.write(textwrap.dedent(conftest_py_content))


@pytest.fixture
def tf_init_test(pytester, sample_skeleton, example_name):
    tf_init_test_content = """
    def test_should_pass(tf_init):
        pass
    """
    tf_init_test_py = pytester.path / "tests" / example_name / "test_tf_init.py"
    with tf_init_test_py.open("w") as f:
        f.write(textwrap.dedent(tf_init_test_content))

    return tf_init_test_py


pytest_plugins = ["pytester"]
