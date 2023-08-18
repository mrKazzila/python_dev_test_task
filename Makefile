# Prepare local env
prepare_env:
	touch env/.env && echo \
"\
# ===== BASE SETTINGS =====\n\
DJANGO_LOG_LEVEL=INFO\n\
DJANGO_DEBUG=True\n\
DJANGO_SECRET_KEY=M!VJM>WQQ#~0)@kp+!n.:RT?hL(#Q/H(\gEzoyHRCB?n8H-\{eH]ZhRu@cbD{a)~HKuo3w#y>UL4qX(GPgMN\n\
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost\n\n\
# ===== DATABASE SETTINGS =====\n\
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2\n\
DATABASE_HOST=127.0.0.1\n\
DATABASE_PORT=5432\n\
DATABASE_NAME=enhance_review_db\n\
DATABASE_USER=postgres\n\
DATABASE_PASSWORD=postgres\n\
" > env/.env

	touch env/.env.db && echo \
   "\
POSTGRES_DB=enhance_review_db\n\
POSTGRES_USER=postgres\n\
POSTGRES_PASSWORD=postgres\
" > env/.env.db

poetry_setup:
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install


# Run project local
django_run:
	python app/manage.py makemigrations
	python app/manage.py migrate
	python app/manage.py runserver


# Testing
test:
	pytest app .

test_linters:
	pre-commit install
	pre-commit run --all-files

docker_run:
	docker-compose -f docker-compose.yaml up -d --build

docker_stop:
	docker-compose -f docker-compose.yaml down -v
