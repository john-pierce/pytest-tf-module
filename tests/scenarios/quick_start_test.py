import shutil

import pytest


@pytest.mark.acc
def test_can_run_quick_start_from_readme_instructions(
    module_test_runner, quickstart_example
):
    """
    Verify that an example module is successfully deployed a test passes
    """
    result = module_test_runner.run_example_tests(quickstart_example)

    assert result.all_tests_passed is True
    assert result.number_of_tests == 1
    assert result.exit_code == 0


@pytest.fixture
def quickstart_example(request, pytester):
    source = request.path.parent / "quick_start_example"
    result = pytester.path

    result.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(source), str(result), dirs_exist_ok=True)

    return result


@pytest.fixture
def module_test_runner(pytester):
    return ModuleTestRunner(pytester)


# Utility modules for dsl
class ModuleTestRunner:
    def __init__(self, pytester_instance):
        self.pytester = pytester_instance

    def run_example_tests(self, *args):
        result = self.pytester.runpytest_subprocess()

        return ModuleTestRunnerResult(result)


class ModuleTestRunnerResult:
    def __init__(self, result):
        self.result = result
        self.outcomes: dict = result.parseoutcomes()

    @property
    def all_tests_passed(self):
        nonzero_outcomes = {
            noun: count for noun, count in self.outcomes.items() if count > 0
        }
        return list(nonzero_outcomes.keys()) == ["passed"]

    @property
    def number_of_tests(self):
        return sum(self.outcomes.values())

    @property
    def exit_code(self):
        return self.result.ret


pytest_plugins = "pytester"
