# geolocation_api

## Description
- Purpose of the geolocation_api is to receive AP Scan data, and check if there's any existing results or else gets new data from Google Geolocation API .
- There's also some functionality to get older results for future reference.

## Requirements
   - Django==3.1.5
   - requests==2.25.1
   - psycopg2==2.8.6
   - environs==9.3.0
   - djangorestframework==3.12.2
   - responses==0.12.1

### Getting Started
Run to create a environment file from the commited template:
```bash
brew install pyenv pyenv-virtualenv
pyenv install 3.8.0
cp .env.template .env
pyenv virtualenv 3.8.0 geolocation
pip install -r requirements.txt
```
Edit the .env on your local machine to point to the correct hosts.

### Setting up the DB
Run to create a environment file from the commited template:
```bash
psql -h 127.0.0.1 -p 5432
CREATE DATABASE geolocation;
python manage.py makemigrations
python manage.py migrate
```

This might mean changing things like the postgres host from `postgres` to `localhost` and
the port number to a serving postgres port which could be running either locally at `5432`

---
### Tests
Unit tests are done through django's test framework and can be run with:

```bash
./manage.py test
```

To run with responses first install the dev requirements:

```bash
pip install -r "requirements.dev.txt"
```

then run:
```bash
coverage run ./manage.py test automated_tests/
```
To get a pretty report you can run:
```bash
coverage html
```
and then open up the generated `htmlcov/index.html` in your browser.

---
Run the following to ensure that migrations have been completed and that the Geolocation
app is live:
```bash
python manage.py migrate
python manage.py runserver
```


[Geolocation API Specifications](https://github.com/Jaques08/geolocation/wiki/API-Usage)