# Installation

install: env_file install_dependencies db

.PHONY:db
db: createdb migrate superuser

.PHONY:env_file
env_file:
	cp .env.example .env.dev

.PHONY:createdb
createdb:
	createdb reciply

# Django management commands

.PHONY:server
server:
	python manage.py runserver 8000 --configuration=Settings

.PHONY:server_https
server_https:
	# Install a local certificate authority so that the OS will trust ours
	mkcert -install
	# Generate a certificate for the localhost domain
	mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
	python manage.py runserver_plus 8000 --configuration=Settings --cert-file=cert.pem --key-file=key.pem

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

# Python environment

install_dependencies: app_dependencies dev_dependencies test_dependencies editable_mode

.PHONY:editable_mode
editable_mode:
	pip install -e .

.PHONY:app_dependencies
app_dependencies:
	pip install -r requirements/app-requirements.txt

.PHONY:dev_dependencies
dev_dependencies:
	pip install -r requirements/dev-requirements.txt

.PHONY:test_dependencies
test_dependencies:
	pip install -r requirements/test-requirements.txt


# CI checks

local_ci: test lint

.PHONY:test
test:
	pytest .

lint: mypy black isort flake8

.PHONY:mypy
mypy:
	mypy ./src

.PHONY:black
black:
	black .

.PHONY:isort
isort:
	isort . --profile=black

.PHONY:flake8
flake8:
	flake8 ./src
	flake8 ./tests
