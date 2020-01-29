DC := $(shell which docker-compose)

all: install

install: $(DC)
	docker-compose build


migrate: $(DC)
	docker-compose run --rm django python ./manage.py migrate

runserver: $(DC)
	docker-compose run -p {{cookiecutter.port}}:{{cookiecutter.port}} --rm django python ./manage.py runserver 0.0.0.0:{{cookiecutter.port}}

superuser: $(DC)
	docker-compose run --rm django python ./manage.py createsuperuser

test: $(DC)
	docker-compose run --rm django py.test

shell:
	docker-compose run --rm django python ./manage.py shell

backup:
	docker-compose exec db pg_dump -U postgres -d postgres -f ./db_backups/`date +%Y-%m-%d_%H:%M:%S`.sql

up:
	docker-compose up

app:
	mkdir apps/$(name)
	docker-compose run --rm django python manage.py startapp $(name) apps/$(name)

requirements:
	docker-compose run --rm django pip-compile --output-file /project/requirements.txt /project/requirements.in
