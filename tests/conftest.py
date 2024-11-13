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


pytest_plugins = ["pytester"]
