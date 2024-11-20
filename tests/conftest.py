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
def sample_skeleton(pytester, example_name):
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

    return pytester.path
