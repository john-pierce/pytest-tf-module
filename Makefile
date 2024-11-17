all: check format

format: ruff-format ruff-isort terraform-fmt

check: ruff-check mypy

test: pytest-all check

ruff-format: ruff-fix ruff-isort
	ruff format src tests

ruff-isort: ruff-fix
	ruff check --select I --fix src tests

terraform-fmt:
	terraform fmt -recursive tests/scenarios/quick_start_example

ruff-check:
	ruff check
	ruff check --select I src tests

ruff-fix:
	ruff check --fix

mypy:
	mypy src

pytest: 
	hatch test

pytest-all:
	hatch test -a

build:
	uv build

ci-test-all: 3.10.t 3.11.t 3.12.t 3.13.t

%.t: %
	hatch test -py=$< -q


.PHONY: \
	3.10 \
	3.11 \
	3.12 \
	3.13 \
	all \
	build \
	check \
	format \
	mypy \
	pytest \
	ruff-check \
	ruff-fix \
	ruff-format \
	ruff-isort \
	terraform-fmt \
	test \
	test-all
