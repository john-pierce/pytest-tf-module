import pytest


# The example_path fixture must be "package" scoped.
@pytest.fixture(scope="package")
def example_path(pytestconfig):
    return pytestconfig.rootpath / "examples" / "quick_start"


# You can also set terraform variables here.
@pytest.fixture(scope="package")
def tf_variables():
    return {
        "pass_through": "QuickStart",
    }
