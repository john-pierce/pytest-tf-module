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


pytest_plugins = ["pytester"]
