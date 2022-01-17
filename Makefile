# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

PYTHON	:= /usr/bin/env python3
MANAGE_PY   := $(PYTHON) manage.py
PYTHON_PIP  := /usr/bin/env pip3
PIP_COMPILE := /usr/bin/env pip-compile
PART := patch
PACKAGE_VERSION = $(shell $(PYTHON) setup.py --version)

# Put it first so that "make" without argument is like "make help".
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-32s-\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help

guard-%: ## Checks that env var is set else exits with non 0 mainly used in CI;
	@if [ -z '${${*}}' ]; then echo 'Environment variable $* not set' && exit 1; fi

# --------------------------------------------------------
# ------- Python package (pip) management commands -------
# --------------------------------------------------------
clean-build: ## Clean project build artifacts.
	@echo "Removing build assets..."
	@$(PYTHON) setup.py clean
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

install: clean-build  ## Install project dependencies.
	@echo "Installing project in dependencies..."
	@$(PYTHON_PIP) install -r requirements.txt

install-lint: clean-build  ## Install lint extra dependencies.
	@echo "Installing lint extra requirements..."
	@$(PYTHON_PIP) install -e .'[lint]'

install-test: clean-build  ## Install test extra dependencies.
	@echo "Installing test extra requirements..."
	@$(PYTHON_PIP) install -e .'[test]'

install-dev: clean-build  ## Install development extra dependencies.
	@echo "Installing development requirements..."
	@$(PYTHON_PIP) install -e .'[development]' -r requirements.txt

update-requirements:  ## Updates the requirement.txt adding missing package dependencies
	@echo "Syncing the package requirements.txt..."
	@$(PIP_COMPILE)

# ----------------------------------------------------------
# --------- Django manage.py commands ----------------------
# ----------------------------------------------------------
run: compilemessages makemessages  ## Run the run_server using default host and port
	@$(MANAGE_PY) runserver 127.0.0.1:8090

migrate:  ## Run the migrations
	@$(MANAGE_PY) migrate

migrations:  ## Generate the migrations
	@$(MANAGE_PY) makemigrations

makemessages: clean-build  ## Runs over the entire source tree of the current directory and pulls out all strings marked for translation.
	@$(MANAGE_PY) makemessages --locale=en_US --ignore=".tox*" --ignore="venv*"
	@$(MANAGE_PY) makemessages --locale=fr --ignore=".tox*" --ignore="venv*"

compilemessages: clean-build  ## Compiles .po files created by makemessages to .mo files for use with the built-in gettext support.
	@$(MANAGE_PY) compilemessages --ignore=".tox*" --ignore="venv*"

# ----------------------------------------------------------
# ---------- Release the project to PyPI -------------------
# ----------------------------------------------------------
increase-version: guard-PART  ## Increase project version
	@bump2version $(PART)
	@git switch -c main

dist: clean install-deploy  ## builds source and wheel package
	@pip install twine==3.4.1
	@python setup.py sdist bdist_wheel

release: dist  ## package and upload a release
	@twine upload dist/*

# ----------------------------------------------------------
# --------- Run project Test -------------------------------
# ----------------------------------------------------------
test: install-test
	@pytest -v

tox: install-test  ## Run tox test
	@tox

clean-test-all: clean-build  ## Clean build and test assets.
	@rm -rf .tox/
	@rm -rf .pytest_cache/
	@rm -f test.db

lint:
	isort .
	flake8 .

create-docs:
	@npx docsify init ./docs

serve-docs:
	@npx docsify serve ./docs

clean: clean-test-all clean-build
