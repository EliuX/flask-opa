# Made by EliuX for OPA-Flask.

.PHONY: build
build: install-dev lint coverage

.PHONY: start-opa
start-opa:
	nohup opa run -s -w examples &

.PHONY: stop-opa, kill
stop-opa:
	kill $(ps | grep opa | awk '{print $1}')

.PHONY: demo
demo: start-opa 
	export FLASK_ENV=development
	export FLASK_APP=examples/app.py
	flask run

.PHONY: test
test:
	pytest -v

.PHONY: coverage
coverage:
	coverage erase
	coverage run -m pytest -v

.PHONY: lint
lint:
	flake8 flask_opa.py --count

.PHONY: install
install:
	pip3 install -e .

.PHONY: install-dev
install-dev: install
	pip3 install --upgrade pytest
	pip3 install --upgrade coverage
	pip3 install --upgrade codecov
	pip3 install --upgrade flake8
	pip3 install --upgrade responses
	pip3 install --upgrade python-semantic-release

.PHONY: semver-test
semver-test:
	semantic-release version --noop

.PHONY: push
push:
	./setup.py sdist bdist_wheel
	pip3 install --user --upgrade twine
	twine upload --repository-url https://pypi.org/legacy/ dist/*

.PHONY: push-test
push-test:
	./setup.py sdist bdist_wheel
	pip3 install --user --upgrade twine
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: help
help: 
	@echo "make start-opa"
	@echo "       starts the opa server"
	@echo "make stop-opa"
	@echo "       stops the opa server" 
	@echo "make demo"
	@echo "       runs the demo project"
	@echo "make test"
	@echo "       run tests"
	@echo "make coverage"
	@echo "       runs the tests and coverage"
	@echo "make lint"
	@echo "      run lints of interest for the code"
	@echo "make install"
	@echo "      install all requirements"
	@echo "make install-dev"
	@echo "      install all requirements for development"
	@echo "make build"
	@echo "      runs lints, tests and coverage"
	@echo "semver-test"
	@echo "      Checks whether the SEMVER update can be done"
