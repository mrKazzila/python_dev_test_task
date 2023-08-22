# Prepare local env
prepare_env:
	touch env/.env2 && echo \
"\
# ===== BASE SETTINGS =====\n\
DJANGO_LOG_LEVEL=INFO\n\
DJANGO_DEBUG=True\n\
DJANGO_SECRET_KEY=M!VJM>WQQ#~0)@kp+!n.:RT?hL(#Q/H(\gEzoyHRCB?n8H-\{eH]ZhRu@cbD{a)~HKuo3w#y>UL4qX(GPgMN\n\
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost\n\
DOMAIN_NAME=\n\n\
# ===== DATABASE SETTINGS =====\n\
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2\n\
DATABASE_HOST=your_host\n\
DATABASE_PORT=your_port\n\
DATABASE_NAME=your_db\n\
DATABASE_USER=your_db_user\n\
DATABASE_PASSWORD=your_db_user_pass\n\n\
# ===== REDIS SETTINGS =====\n\
REDIS_HOST=redis\n\
REDIS_PORT=6379\n\n\
# ===== CELERY SETTINGS =====\n\
CELERY_SCHEDULE_TIME_MINUTES=*/1\n\n\
# ===== EMAIL SETTINGS =====\n\
EMAIL_HOST=smtp.gmail.com\n\
EMAIL_PORT=587\n\
EMAIL_USE_TLS=True\n\
EMAIL_HOST_USER=your_email\n\
EMAIL_HOST_PASSWORD=your_email\n\n\
# ===== RECAPTCHA SETTINGS =====\n\
RECAPTCHA_PUBLIC_KEY=your_public_key\n\
RECAPTCHA_PRIVATE_KEY=your_private_key\
" > env/.env2

	touch env/.env2.db && echo \
   "\
POSTGRES_DB=your_db\n\
POSTGRES_USER=your_db_user\n\
POSTGRES_PASSWORD=your_db_user_pass\
" > env/.env2.db

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

docker_reload:
	make docker_stop
	make docker_run

# Prod
docker_prod_run:
	docker-compose -f docker-compose.yaml up -d --build

docker_prod_stop:
	docker-compose -f docker-compose.yaml down

docker_prod_stop_remove_volumes:
	docker-compose -f docker-compose.yaml down -v

enter_to_container_name:
	docker-compose -f docker-compose.prod.yaml exec $(name) bash

docker_remove_all_force:
	sudo docker-compose -f docker-compose.prod.yaml down -v && \
	sudo docker rmi --force $(sudo docker images -aq) && \
	docker volume prune && \
	docker system prune
