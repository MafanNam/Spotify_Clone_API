# Spotify_Clone_API

This is the repository for the Spotify_Clone_API project, which is a clone of the Spotify web service. This API
implements
a basic set of functionalities allowing users to interact with the platform.

![Spotify title](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/spotify_data_flow.svg)

### Diagram DB

![Spotify diagram DB](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/db_diagram.svg)

## Description

Spotify_Clone_API is developed using Django, one of the most popular frameworks for building web applications in Python.
This API provides features such as user registration, advertisement creation, user profile management, and other core
functionalities.

![Spotify front](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/spotify_front.png)

## Requirements

To run this API, you'll need:

- Python 3.11
- Django v5
- Django REST Framework
- and other dependencies listed in the `requirements.txt` file

## Installation and Running

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/MafanNam/Spotify_Clone_API.git
```

2. Navigate to the project directory:

```bash
$ cd Spotify_Clone_API
```

3. Create/Activate environment:

```bash
$ pip install virtualenv
$ python -m virtualenv venv
$ .\venv\Scripts\activate
$ # or linux
$ source venv/bin/activate
```

4. Install dependencies:

```bash
$ pip install -r requirements/local.txt
```

5. Apply migrations to create the database:

```bash
$ python manage.py migrate
```

6. Load example data `NOT COMPLETE`

```bash
$ python -Xutf8 ./manage.py loaddata data/mydata.json
```

7. Run the server:

```bash
$ python manage.py runserver
```

#### About fixtures(mydata.json)

All user email in [data/mydata.json](mydata.json) and `password=Pass12345`

for admin user `email=admin@gmail.com` and `password=1`

### If you want the api to send messages to mail

Then you MUST create and config `django.env` optional `django.docker.env`.

For example I create `django.example.env` and `django.docker.example.env`

All these files are in [.envs/.local/](.envs/.local/)

You can now access the API in your browser at http://localhost:8000/.

## Getting Started with Docker

Commands can be run through a makefile or written manually.

You can access the API in your browser at http://localhost:8080/. Flower http://localhost:5555/

### To build and raise a container, you just need to run it:

You cannot use makefile

```bash
$ docker compose -f local.yml up --build -d --remove-orphans
$ # or
$ docker compose -f local.yml up --build
```

You can use makefile

```bash
$ make build
$ # or
$ make build-log
```

### Basic commands:

```bash
$ make buld-log

$ make up

$ make down
```

## Run test

For testing and generate coverage

![cov tests]()

#### makefile

```bash
$ make cov
$ make cov-gen
```

`Docker`

```bash
$ make cov-docker
$ make cov-gen-docker
```

#### no makefile

```bash
$ coverage run --source='.' --omit='*/migrations/*.py,*/asgi.py,*/wsgi.py,*/manage.py' manage.py test
$ coverage html
```

`Docker`

```bash
$ docker compose -f local.yml run --rm server coverage run --source='.' --omit='*/migrations/*.py,*/asgi.py,*/wsgi.py,*/manage.py' manage.py test
$ docker compose -f local.yml run --rm server coverage html
```

## API Documentation

The API documentation is not available [localhost:8080](http://localhost:8080).

![Spotify swagger](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/swagger.png)
![Spotify redoc](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/redoc.png)

## Custom Admin

![Spotify admin](https://raw.githubusercontent.com/MafanNam/Spotify_Clone_API/main/assets/admin.png)

## Author

This project is developed by Mafan.

## License

This project is licensed under MIT License.
