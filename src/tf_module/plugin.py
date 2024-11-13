import pytest


def pytest_configure(config: pytest.Config):
    config.option.log_cli = True
    config.option.log_cli_level = "INFO"
