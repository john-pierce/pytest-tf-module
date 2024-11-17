import pathlib
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


@pytest.mark.parametrize(
    "example_path_conftest",
    [
        "absolute_example_path_conftest",
        "relative_example_path_conftest",
    ],
    indirect=True,
)
def test_tf_example_path_can_be_relative_to_project_root(
    pytester, example_path_conftest
):
    result = pytester.runpytest_subprocess()
    result.assert_outcomes(passed=1)

    result.stdout.no_fnmatch_line("*empty directory!*")

    result.stdout.fnmatch_lines(
        [
            "*has been successfully initialized*",
        ]
    )


@pytest.fixture
def example_path_conftest(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def absolute_example_path_conftest(
    pytester,
    example_path_relative_path,
    example_path_tests_path,
    example_path_tests_structure,
):
    conftest_py_content = """
    import pytest
    @pytest.fixture
    def example_path(pytestconfig):
        return pytestconfig.rootpath / "{relative_path}"
    """.format(relative_path=example_path_relative_path)
    with (pytester.path / example_path_tests_path / "conftest.py").open(
        "w"
    ) as conftest_py:
        conftest_py.write(textwrap.dedent(conftest_py_content))


@pytest.fixture
def relative_example_path_conftest(
    pytester,
    example_path_relative_path,
    example_path_tests_path,
    example_path_tests_structure,
):
    conftest_py_content = """
    import pytest, pathlib
    @pytest.fixture
    def example_path(request):
        return pathlib.Path("{relative_path}")
    """.format(relative_path=example_path_relative_path)
    with (pytester.path / example_path_tests_path / "conftest.py").open(
        "w"
    ) as conftest_py:
        conftest_py.write(textwrap.dedent(conftest_py_content))


@pytest.fixture
def example_path_relative_path():
    return pathlib.Path("examples/path_test_example")


@pytest.fixture
def example_path_tests_path():
    return pathlib.Path("tests/path_test_example")


@pytest.fixture
def example_path_tests_structure(
    pytester, example_path_relative_path, example_path_tests_path
):
    examples_path = pytester.path / example_path_relative_path
    examples_path.mkdir(parents=True)
    (examples_path / "main.tf").touch()

    tests_path = pytester.path / example_path_tests_path
    tests_path.mkdir(parents=True)

    with (tests_path / "test_pass.py").open("w") as test_file:
        test_file_content = """
        from tf_module.plugin import run_terraform_command
        def test_pass(example_path):
            run_terraform_command("init", workdir=example_path)
        """
        test_file.write(textwrap.dedent(test_file_content))

    pytest_ini = pytester.path / "pytest_ini"
    pytest_ini.touch()
