# Local dev

.PHONY:server
server:
	python reciply/manage.py runserver 8000 --configuration=Settings

.PHONY:db
db: createdb migrate su

.PHONY:new_db
new_db: dropdb createdb migrate su

.PHONY:migrate
migrate:
	python reciply/manage.py migrate --configuration=Settings

.PHONY:migrations
migrations:
	python reciply/manage.py makemigrations --configuration=Settings

.PHONY:su
su:
	DJANGO_SUPERUSER_PASSWORD=password python reciply/manage.py createsuperuser --configuration=Settings --username=edwilson543 --email=fake@example.com --no-input

.PHONY:createdb
createdb:
	createdb reciply

.PHONY:dropdb
dropdb:
	dropdb reciply

# CI checks

local_ci: test lint

.PHONY:test
test:
	pytest .

lint: mypy black isort flake8

.PHONY:mypy
mypy:
	mypy ./reciply

.PHONY:black
black:
	black .

.PHONY:isort
isort:
	isort . --profile=black

.PHONY:flake8
flake8:
	flake8 ./reciply
	flake8 ./tests
