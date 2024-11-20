import random
import string
import textwrap

import pytest


@pytest.fixture(autouse=True)
def use_plugin(pytester):
    # Appending to pytester.plugins breaks PyCharm's debugger.
    pytester.makeini(
        """
        [pytest]
        addopts = -p tf_module.plugin
        """
    )


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


@pytest.fixture
def example_name():
    """
    Random name to be used as part of a test skeleton
    :return:
    """
    return "".join(random.choices(string.ascii_letters, k=6))


@pytest.fixture
def sample_skeleton(request, pytester, example_name):
    """
    Creates a sample plugin with no tests or conftest.
    """
    example_dir = pytester.path / "examples" / example_name
    example_dir.mkdir(parents=True)
    example_main_tf_path = example_dir / "main.tf"
    with example_main_tf_path.open("w") as f:
        example_main_tf_content = """
        module "sample" {
            source = "../.."
        }
        """
        f.write(textwrap.dedent(example_main_tf_content))

    example_tests_dir = pytester.path / "tests" / example_name
    example_tests_dir.mkdir(parents=True)

    module_main_tf_path = pytester.path / "main.tf"
    with module_main_tf_path.open("w") as f:
        module_main_tf_content = """
        resource "null_resource" "this" {}
        """
        f.write(textwrap.dedent(module_main_tf_content))

    request.getfixturevalue("sample_conftest")

    return pytester.path


@pytest.fixture
def sample_conftest(pytester, example_name):
    """
    This is intended to be invoked by sample_skeleton, not requested directly.

    Redefine this at the module level to override the default.
    """
    conftest_py_path = pytester.path / "tests" / example_name / "conftest.py"
    with conftest_py_path.open("w") as f:
        conftest_py_content = f"""
        import pytest
        @pytest.fixture(scope="package")
        def example_path(pytestconfig):
            return pytestconfig.rootpath / "examples" / "{example_name}"
        """
        f.write(textwrap.dedent(conftest_py_content))

    return conftest_py_path
