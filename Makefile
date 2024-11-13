all: format check

format: ruff_format ruff_isort terraform_fmt

check: ruff_check mypy

ruff_format:
	ruff format src tests

ruff_isort:
	ruff check --select I --fix src tests

terraform_fmt:
	terraform fmt -recursive tests/scenarios/quick_start_example

ruff_check:
	ruff check

ruff_fix:
	ruff check --fix

mypy:
	mypy src



.PHONY: all format check ruff_format terraform_fmt ruff_check mypy
