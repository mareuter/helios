.PHONY: help
help:
	@echo "Availble make targets:"
	@echo "make init - Initialize environment"

.PHONY: init
init:
	python -m pip install --upgrade pip
	pip install -e .[dev]
