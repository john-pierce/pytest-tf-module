pytest-tf-module
----------------

pytest plugin for end-to-end testing of terraform modules.

The tf-module plugin provides several fixtures for testing terraform
modules by testing the deployed resources using examples. It aims to aid in
incremental development of a module by building out and testing a functional
example.

This took inspiration from (See the [FAQ](#faq)):
 * [Terratest](https://terratest.gruntwork.io/)
 * [tftest](https://pypi.org/project/tftest/)
 * [pytest-terraform](https://pypi.org/project/pytest-terraform/)

Features:

This plugin focuses only on the essentials of running Terraform. It does not
provide helpers for higher level functionality or access to Terraform
internals.

- [x] Display terraform output in real time
  - [x] `init`
  - [x] `apply`
  - [x] `destroy`
  - [x] `output`
  - [ ] Allow skipping of each step
- [ ] Flight recorder (caching)
  - [ ] Automatic invalidation
- [ ] Idempotency validation


## Quick Start

Install from GitHub with
`pip install https://github.com/john-pierce/pytest-tf-module`.


### Specify Example Locations

Use the example_path fixture at the test package level:

```
.
├── pytest.ini     <───── May be empty, used to establish the project root
├── examples
│   ├── quick_start          <───── Name of the example
│   │   ├── main.tf
:   :   :
├── tests
│   ├── quick_start          <───── This name doesn't matter
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_features.py
:   :   :
```

#### Establish the path to your example in your test package:

```python
# tests/quick_start/conftest.py
import pytest

# The example_path fixture must be "package" scoped.
@pytest.fixture(scope="package")
def example_path(pytestconfig):
    return pytestconfig.rootpath / "examples" / "quick_start"

# Plugin must be explicitly activated
pytest_plugins = ["tf_module"]
```

#### Define variables to be passed to terraform:

```python
# tests/quick_start/conftest.py
import pytest

def example_path(pytestconfig): ...
 
@pytest.fixture(scope="package")
def tf_variables():
  return {
    "pass_through": "QuickStart",
  }
```

#### Write your tests:

```python
# tests/complete/test_start.py

def test_passthrough(tf_outputs, tf_variables):
    assert tf_outputs["pass_through"] == tf_variables["pass_through"]
```

#### Run your tests (from the project root):

```shell
$ pytest

# Placeholder for output after the example test is finished.
```

## Fixtures

Because examples are tested at the package level, all fixtures have the
"package" scope unless otherwise noted.

### User defined fixtures

These are fixtures that can be defined to influence the behavior of the
plugin. Of these only `example_path` is mandatory.

#### example_path

`example_path` must be defined for each test package. It should return a
path to Terraform's `path.root` of the example. The path may be absolute or
relative to the project's root. See the quick start
[example_path](#establish-the-path-to-your-example-in-your-test-package).

#### tf_variables

The `tf_variables` fixture can be defined to pass variables to Terraform.
It should return a dictionary in the form `{ "variable_name": "value" }`.
See the quick_start [tf_variables](#define-variables-to-be-passed-to-terraform)
definition.


### Plugin provided fixtures

These fixtures execute Terraform commands and unless otherwise specified,
return a string containing the output from stdout of the `terraform` command.

If any command fails it will generate a `TFExecutionError` and stderr will
be logged _after_ terraform exits.

### tf_init

Requesting the `tf_init` fixture will cause `terraform init` to be run in
the example directory specified by the [example_path](#example_path)
fixture.

Only the local backend is supported.

Specifying `--skip init` will skip execution of `terraform init`.

### tf_apply 

Requesting the `tf_apply` fixture will cause `terraform apply` to be run in
the example directory. `tf_apply` requests `tf_init` causing
`terraform init` to run prior to applying the example configuration.

Variables can be passed to terraform by defining the
[tf_variables](#tf_variables) fixture at the package level.

By default, `tf_apply` will request [tf_destroy](#tf_destroy) which will destroy
resources from the example configuration.

Specifying `--skip apply` will skip the execution of `terraform apply`.

### tf_destroy

Requesting the `tf_destroy` fixture causes `terraform destroy` to be run in
the example directory during the teardown phase.

`tf_apply` does not need to be requested in order to request `tf_destroy`.
It is a dependency of `tf_apply`,

This fixture returns None because terraform isn't run until terardown.
Any terraform output will still be logged and printed to stdout.

Specifying `--skip destroy` will skip the execution of `terraform destroy`.

### tf_output

Requesting the `tf_output` fixture returns a dictionary representing the
output of `terraform output`. Only the `value` of each output is stored in
the resulting dictionary. Sensitive values are not treated specially and
will be available, unmasked, in the returned dictionary.

Objects, maps and lists will be returned as native Python dictionaries and
lists respectively.

> [!NOTE]
> Terraform outputs lists as lists of strings, regardless of the element's
> type. List `tf_output` values are of List[str] type.

`tf_output` requests `tf_apply` and is often the only fixture needed.

Specifying `--skip destroy` will skip the execution of `terraform destroy`
and return and empty dictionary.


## FAQ

#### What are examples?

Examples are complete configurations that demonstrate the use of the
module under test. It's common to have a "complete" example that utilizes as
much of the module's functionality as possible. These can be used to drive
feature development of the module.

Each example is a standalone configuration that will be applied at the test
package level.

#### Why another Terraform pytest plugin?

I wanted to be able to work with the common module structure from the
[terraform-aws-modules](https://github.com/terraform-aws-modules)
collection, including multiple examples and submodules. I really like
[terratest](https://terratest.gruntwork.io/), but I find boto3 much easier
to write tests in than the Go AWS SDK.

[tftest](https://pypi.org/project/tftest/) is essentially a wrapper
for running terraform with some very nice extras which may be carried over.
I ultimately wanted a bit less encoded logic and more flexibility with
stage caching.

[pytest-terraform](https://github.com/cloud-custodian/pytest-terraform) has
the behavior of destroying resources if an apply fails. This is undesirable
for my workflow which largely involves using tests as fitness functions for
my configuration "experiments". Having to tear down and stand up every
resource every time I make a bad change is painful at best.

This is the result of minimally building this as I need it.