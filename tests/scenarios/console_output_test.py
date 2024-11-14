from collections import namedtuple

import pytest


@pytest.mark.filterwarnings("ignore:.*multi-threaded.*forkpty:DeprecationWarning")
def test_terraform_output_should_be_shown_in_realtime(
    scroll_detector, scrolling_runner
):
    """
    When the terraform command is run, the pytest cli should print the output
    of the command to the console in real time rather than at the end of the test.
    """
    assert scroll_detector.detects_scroll_from(scrolling_runner)


ScrollDetector = namedtuple("ScrollDetector", "detects_scroll_from")


@pytest.fixture
def scroll_detector(controlled_expect_script):
    """
    Run an expect script to check the output of a pytest process that simulates
    real-time scroll.
    """

    def detects_scroll_from(child):
        return controlled_expect_script(child) is True

    return ScrollDetector(detects_scroll_from)


@pytest.fixture
def scrolling_runner(pytester, scroll_test_path):
    """
    Runs a test that will produce real-time scrolling with the plugin loaded.
    """
    pytester.makeini("[pytest]\naddopts = -p tf_module.plugin\n")

    with pytester.spawn_pytest(str(scroll_test_path), expect_timeout=2) as child:
        yield child


@pytest.fixture
def controlled_expect_script(control_file_path):
    """
    Write to a control file that the test fixture will "tail". The child should
    echo back every line written to the control file until TAIL_END.
    """

    def run(child):
        # print(child.read())  # Useful for debugging but will break the test
        with open(control_file_path, "a") as cf:
            child.expect("Initial log entry")

            cf.write("New log entry\n")
            cf.flush()

            child.expect("New log entry")
            cf.write("TAIL_END\n")

        child.expect("Test f entry")

        return True

    return run


@pytest.fixture
def scroll_test_path(pytester, control_file_path):
    """
    Loads a fixture that tails a file until "TAIL_END". This file is expected to be
    appended to by the scroll detector to produce output on demand.
    """

    test_script = """
        import time, logging, pytest
        log = logging.getLogger("scroller")
        @pytest.fixture
        def tail_f():
            cf = open("{control_file}")
            log.info("opening {control_file}")
            while True:
                line = cf.readline()
                if line.strip() == "TAIL_END":
                    break
                elif line:
                    log.info(line)
                else:
                    time.sleep(0.01)
        def test_f(tail_f):
            log.info("Test f entry")
    """.format(control_file=control_file_path)

    return pytester.makepyfile(test_script)


@pytest.fixture
def control_file_path(pytester):
    return pytester.makefile(".tail", "Initial log entry")


pytest_plugins = ["pytester"]
