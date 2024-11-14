all: format check

format: ruff_format ruff_isort terraform_fmt

check: ruff_check mypy

test: pytest_all check

ruff_format:
	ruff format src tests

ruff_isort:
	ruff check --select I --fix src tests

terraform_fmt:
	terraform fmt -recursive tests/scenarios/quick_start_example

ruff_check:
	ruff check
	ruff check --select I src tests

ruff_fix:
	ruff check --fix

mypy:
	mypy src

pytest: 
	hatch test

pytest_all:
	hatch test -a

build:
	uv build

.PHONY: all \
	build \
	check \
	format \
	mypy \
	pytest \
	ruff_check \
	ruff_fix \
	ruff_format \
	ruff_isort \
	terraform_fmt \
	test
