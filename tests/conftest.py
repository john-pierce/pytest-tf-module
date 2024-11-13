import pytest


@pytest.fixture(autouse=True)
def use_plugin(pytester):
    pytester.plugins.append("tf-module.plugin")


pytest_plugins = ["pytester"]
