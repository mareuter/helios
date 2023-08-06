.PHONY: help
help:
	@echo "Availble make targets:"
	@echo "make init - Initialize environment"
	@echo "make init-pre-commit - Initialize dev envrionment with pre-commit"
	@echo "make init-clone - Initialize a fresh clone"
	@echo "make update-submodule - Update the pre-commit config submodule"

.PHONY: init
init:
	python -m pip install --upgrade pip
	pip install -r requirements/test.txt
	python bin/setup_skyfield.py

.PHONY: init-pre-commit
init-pre-commit:
	python -m pip install --upgrade pip
	pip install pre-commit
	./pre-commit-config/setup_pre_commit_config.py  --mypy-extras=`cat requirements/mypy-extras.txt`

.PHONY: init-clone
init-clone:
	git submodule init
	git submodule update
	make init
	make init-pre-commit

.PHONY: update-submodule
update-submodule:
	git submodule update --remote
	./pre-commit-config/setup_pre_commit_config.py  --mypy-extras=`cat requirements/mypy-extras.txt`
