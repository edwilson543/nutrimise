# Installation

install: install_pre_commit env_file install_dev_deps db

.PHONY:db
db: createdb migrate superuser

.PHONY:new_db
new_db: dropdb createdb migrate superuser import_snapshot

.PHONY:env_file
env_file:
	cp .env.example .env

.PHONY:createdb
createdb:
	createdb nutrimise

.PHONY:dropdb
dropdb:
	dropdb nutrimise

.PHONY:install_pre_commit
install_pre_commit:
	pre-commit install

# Django management commands

.PHONY:server
server:
	make snapshot
	python manage.py runserver 8000 --configuration=Settings

.PHONY:migrate
migrate:
	python manage.py migrate --configuration=Settings

.PHONY:migrations
migrations:
	python manage.py makemigrations --configuration=Settings

.PHONY:superuser
superuser:
	DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --configuration=Settings --username=edwilson543 --email=fake@example.com --no-input

.PHONY:snapshot
snapshot:
	python manage.py dumpdata ingredients recipes menus auth.user --configuration=Settings --output=data/snapshot.json

.PHONY:import_snapshot
import_snapshot:
	python manage.py loaddata data/snapshot.json

.PHONY:load_example_data
load_example_data:
	python manage.py import_from_csv --dataset=example

.PHONY:load_target_data
load_target_data:
	python manage.py import_from_csv --dataset=target

# Python environment

.PHONY:install_ci_deps
install_ci_deps:
	pip install -r requirements/ci-requirements.txt
	pip install -e .

# Install all dependencies, for local dev.
.PHONY:install_deps
install_deps:
	pip install -r requirements/dev-requirements.txt
	pip install -e .


.PHONY:lock_deps
lock_deps:
	pip install pip-tools
	pip-compile pyproject.toml -q --resolver=backtracking --output-file=requirements/app-requirements.txt
	pip-compile pyproject.toml -q --resolver=backtracking --extra=ci --output-file=requirements/ci-requirements.txt
	pip-compile pyproject.toml -q --resolver=backtracking --extra=ci --extra=dev --output-file=requirements/dev-requirements.txt

# CI checks

local_ci: test lint

.PHONY:test
test:
	pytest .

lint: mypy check lint_imports

.PHONY:mypy
mypy:
	mypy .

.PHONY:format
format:
	ruff format .
	ruff check . --fix

.PHONY:check
check:
	ruff format . --check
	ruff check .

.PHONY:lint_imports
lint_imports:
	lint-imports

# Docker

docker_server: docker_image docker_run

.PHONY:docker_run
docker_run:
	docker container run -p 8000:8000 --name=nutrimise nutrimise:latest

.PHONY:docker_image
docker_image:
	docker image build . -t nutrimise:latest
