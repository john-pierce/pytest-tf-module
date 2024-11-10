def pytest_configure(config):
    config.log_cli = True
    config.option.log_cli_level = "INFO"
