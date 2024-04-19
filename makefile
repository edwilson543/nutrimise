# Installation

install: env_file install_dev_deps db

.PHONY:db
db: createdb migrate superuser

.PHONY:env_file
env_file:
	cp .env.example .env

.PHONY:createdb
createdb:
	createdb nutrimise

# Django management commands

.PHONY:server
server:
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

.PHONY:dump
dump:
	python manage.py dumpdata ingredients recipes menus --configuration=Settings --output=data/dump.json

.PHONY:load
load:
	python manage.py loaddata dump.json

# Python environment

.PHONY:install_ci_deps
install_ci_deps:
	pip install -r requirements/ci-requirements.txt
	pip install -e .

.PHONY:install_dev_deps
install_dev_deps:
	pip install -r requirements/dev-requirements.txt
	pip install -e .


.PHONY:lock_dependencies
lock_dependencies:
	pip-compile pyproject.toml -q --resolver=backtracking --output-file=requirements/app-requirements.txt
	pip-compile pyproject.toml -q --resolver=backtracking --extra=ci --output-file=requirements/ci-requirements.txt
	pip-compile pyproject.toml -q --resolver=backtracking --extra=ci --extra=dev --output-file=requirements/dev-requirements.txt

# CI checks

local_ci: test lint

.PHONY:test
test:
	pytest .

lint: mypy ruff_format ruff_check

.PHONY:mypy
mypy:
	mypy .

.PHONY:ruff_format
ruff_format:
	ruff format .

.PHONY:ruff_check
ruff_check:
	ruff check --fix .

# Docker

docker_server: docker_image docker_run

.PHONY:docker_run
docker_run:
	docker container run -p 8000:8000 --name=nutrimise nutrimise:latest

.PHONY:docker_image
docker_image:
	docker image build . -t nutrimise:latest
