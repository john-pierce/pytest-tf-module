pytest-tf-module
----------------

pytest plugin for end to end testing of terraform modules.

The tf-module plugin provides several fixtures for testing terraform
modules by testing the deployed resources using examples. It aims to aid in
incremental development of a module by building out and testing a functional
example.

This took inspiration from (See the [FAQ](#faq)):
 * [Terratest](https://terratest.gruntwork.io/)
 * [tftest](https://pypi.org/project/tftest/)
 * [tftest](https://pypi.org/project/pytest-terraform/)

Features:

- [x] Display terraform output in real time
- [ ] Allow skipping of
  - [ ] `init`
  - [ ] `apply`
  - [ ] `destroy`
- [ ] Flight recorder (caching)
  - [ ] Automatic invalidation

### Installation

Install with pip directly from GitHub:

```shell
pip install https://github.com/john-pierce/pytest-tf-module
```

## Development

### Requirements

* Python >= 3.10
* [uv](https://docs.astral.sh/uv/)
* GNU Make >= 3.81

### Environment setup

#### Create and activate a venv

You only need to do this part once:

```shell
python -m venv .venv
```


It needs to be activated in every shell you're working with the project in:

```shell
. .venv/bin/activate
````

> [!IMPORTANT]
> Every command from here assumes this venv is active in your shell
 

#### Install uv and development requirements

```pip install uv && uv sync --all-extras```


#### Pre commit

```pre-commit install```

### Tests

#### Running tests

```pytest```


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