import json
import textwrap

import pytest


@pytest.mark.usefixtures("tf_destroy_test")
def test_destroy_leaves_no_resources(pytester, example_name):
    """
    Test that resources are destroyed by the tf_destroy fixture by interrogating
    the .tfstate file in the example directory.
    """
    result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(["*complete! Resources: 1 destroyed."])

    tf_state_path = pytester.path / "examples" / example_name / "terraform.tfstate"
    with tf_state_path.open() as f:
        state = json.load(f)

    assert state["resources"] == []


@pytest.mark.usefixtures("tf_destroy_test")
def test_skip_destroy_skips_tf_apply(pytester):
    result = pytester.runpytest_subprocess("--skip", "destroy")

    result.stdout.no_fnmatch_line("*Destroy complete!*")


@pytest.fixture
def tf_destroy_test(pytester, sample_skeleton, example_name):
    tf_destroy_test_content = """
    import pytest
    @pytest.mark.usefixtures("tf_apply")
    def test_should_destroy(tf_destroy):
        pass
    """
    tf_init_test_py = pytester.path / "tests" / example_name / "test_tf_destroy.py"
    with tf_init_test_py.open("w") as f:
        f.write(textwrap.dedent(tf_destroy_test_content))

    return tf_init_test_py


pytest_plugins = ["pytester"]
