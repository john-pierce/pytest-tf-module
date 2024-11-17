# pytest-tf-module

## Developer Documentation

This document is intended for developers who wish to contribute to this
plugin.

### Requirements

* Python >= 3.10
* [uv](https://docs.astral.sh/uv/)
* GNU Make >= 3.81

### Environment setup

All the common development tasks can be accomplished with `uv run -- ...`
without a virtual environment `uv` is installed globally.

> [!WARNING]
> Running under `pipx`, `hatch` will fail to locate or install the required
> versions of Python for the complete test matrix. Using the virtualenv
> method below or installing `uv` in the current Python environment is 
> recommended.

#### Creation and activation a virtualenv (optional)

Working within a virtualenv may be more familiar and avoids needing to nest
multiple commands every time. One can be created in the top level of this
project by invoking:

```shell
python -m venv .venv
```

It needs to be activated in every shell when working with the project:

```shell
. .venv/bin/activate
````

> [!IMPORTANT]
> If a virtualenv is not being used, the commands that follow need to be
> prefixed with `uv run -- ...`.
> 
> The `--` indicates to `uv` that it should stop processing options and all
> following options should be passed to the subcommand.
 

#### Install uv and development requirements (optional)

`uv` is required for managing dependencies in the virtualenv. It and
other development dependencies can be installed with:

```shell
pip install uv && uv sync --all-extras
```

#### Pre commit

Pre-commit runs basic sanity checks before commiting. These checks must pass
before issuing a PR.

```shell
pre-commit install
```

### Tests

#### Running tests

Tests can be run via `make`, and optionally under all supported version of
Python:

```shell
make pytest[-all]
```

For more specific test selection call `hatch` directly with any `pytest`
options following `--`'s. For example to run only acceptance tests:

```shell
hatch test -- -m acc
```
