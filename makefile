#clean:
#	pre-commit run --all-files
clean:
	pre-commit run --color=always --all-files
build:
	docker compose -f local.yml up --build -d --remove-orphans
build-log:
	docker compose -f local.yml up --build

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs server

#makemigrations:
#	docker compose -f local.yml run --rm server python manage.py makemigrations
#
#migrate:
#	docker compose -f local.yml run --rm server python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm server python manage.py collectstatic --no-input --clear

createsuperuser:
	python manage.py createsuperuser

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

dumpdata:
	python -Xutf8 ./manage.py dumpdata --exclude=auth --exclude=contenttypes --exclude=sessions -o mydata.json

loaddata:
	python -Xutf8 ./manage.py loaddata mydata.json

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect local_postgres_data

spotify-db:
	docker compose -f local.yml exec postgres psql --username=mafan --dbname=spotify-live

cov:
	coverage run --source='.' --omit='*/migrations/*.py,*/asgi.py,*/wsgi.py,*/manage.py' manage.py test
cov-gen:
	coverage html

cov-docker:
	docker compose -f local.yml run --rm server coverage run --source='.' --omit='*/migrations/*.py,*/asgi.py,*/wsgi.py,*/manage.py' manage.py test

cov-gen-docker:
	docker compose -f local.yml run --rm server coverage html
