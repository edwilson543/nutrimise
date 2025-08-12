# Services
.PHONY:server
server:
	make snapshot
	python manage.py runserver 8000 --configuration=Settings

.PHONY:api
api:
	python src/nutrimise/config/asgi.py

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
	python manage.py dumpdata ingredients recipes menus auth.user --configuration=Settings --output=data/snapshots/snapshot.json

.PHONY:import_snapshot
import_snapshot:
	python manage.py loaddata data/snapshots/snapshot.json

.PHONY:load_example_data
load_example_data:
	python manage.py import_from_csv --dataset=example

.PHONY:load_target_data
load_target_data:
	python manage.py import_from_csv --dataset=target

.PHONY:extract_recipes
extract_recipes:
	python manage.py extract_recipes_from_images

.PHONY:recipe_embeddings
recipe_embeddings:
	python manage.py create_recipe_embeddings

.PHONY:nutritional_info
nutritional_info:
	python manage.py gather_ingredient_nutritional_information

# Python environment

.PHONY:install_ci_deps
install_ci_deps:
	uv sync --group ci

# Install all dependencies, for local dev.
.PHONY:install_deps
install_deps:
	uv sync --all-groups


.PHONY:lock_deps
lock_deps:
	uv lock

# CI checks

local_ci: test lint

.PHONY:test
test:
	uv run pytest .

lint: mypy check lint_imports

.PHONY:mypy
mypy:
	uv run mypy .

.PHONY:format
format:
	uv run ruff format .
	uv run ruff check . --fix

.PHONY:check
check:
	uv run ruff format . --check
	uv run ruff check .

.PHONY:lint_imports
lint_imports:
	uv run lint-imports

# Docker

docker_server: docker_image docker_run

.PHONY:docker_run
docker_run:
	docker container run -p 8000:8000 --name=nutrimise nutrimise:latest

.PHONY:docker_image
docker_image:
	docker image build . -t nutrimise:latest
