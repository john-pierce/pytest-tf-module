import subprocess

import pytest


@pytest.mark.usefixtures("minimal_tf_config_dir")
def test_tf_command_can_be_configured(tf_command_name, pytester):
    expected_command = tf_command_name
    test = f"""
    def test_tf_command_is_set(pytestconfig):
        assert "{expected_command}" == pytestconfig.getini("tf_command")
    """

    pytester.makepyfile(test)
    result = pytester.runpytest_inprocess()
    result.assert_outcomes(passed=1)


@pytest.mark.usefixtures("minimal_tf_config_dir")
@pytest.mark.parametrize("tf_command_name", [None], indirect=True)
def test_tf_command_defaults_to_terraform(pytester, tf_command_name):
    test = """
    def test_tf_command_is_terraform(pytestconfig):
        assert "terraform" == pytestconfig.getini("tf_command")
    """
    pytester.makepyfile(test)
    result = pytester.runpytest_inprocess()
    result.assert_outcomes(passed=1)


@pytest.mark.usefixtures("minimal_tf_config_dir", "minimal_test_conftest")
def test_tf_init_calls_configured_command(
    pytester,
    tf_command_name,
    monkeypatch,
):
    """
    Test that pytest calls the command specified by tf_command ini setting.
    """
    test = """
    def test_tf_init(tf_init):
        pass
    """

    popen = subprocess.Popen

    def cmd_called(*args, **kwargs):
        assert tf_command_name == args[0][0]
        return popen("/bin/true")

    pytester.makepyfile(test)

    with monkeypatch.context() as mp:
        mp.setattr(subprocess, "Popen", cmd_called)
        result = pytester.runpytest_inprocess()

    result.assert_outcomes(passed=1)
