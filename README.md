### Backend for the [reciply mobile app](https://github.com/edwilson543/reciply-mobile)

- Django and Django Rest Framework for the API used by the app
- Django Rest Knox for token authentication
- Postgres for the database
- Plugin S3 integration for storing images

---

### Setup:
#### System requirements:
- Python 3.11
- postgres 14.9
- mkcert 1.4.4 (optional)

#### Create database
```bash
createdb reciply
```

#### Install dependencies
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements/app-requirements.txt
pip install -r requirements/dev-requirements.txt
pip install -r requirements/test-requirements.txt
cd reciply
python manage.py migrate
```

#### Create env file
```bash
cp data/.env.example data/.env.dev
```

### Run the development server with HTTP:
```bash
cd reciply
python manage.py runserver 8000 --configuration=Settings
```

### Run the development server with HTTPS:
#### Setup SSL
```bash
# Install a local certificate authority so that the OS will trust ours
mkcert -install

# Generate a certificate for the localhost domain
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```
#### Run the server
```bash
cd reciply
runserver_plus 8000 --configuration=Settings --cert-file=cert.pem --key-file=key.pem
```
