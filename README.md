## Backend for the reciply mobile app

---

## Setup:
### System requirements:
- Python 3.11
- postgres 14.9
- mkcert 1.4.4

### Create database
```bash
createdb reciply
```

### Install dependencies
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements/app-requirements.txt
pip install -r requirements/dev-requirements.txt
pip install -r requirements/test-requirements.txt
cd reciply
python manage.py migrate
```

#### Setup SSL
```bash
# Install a local certificate authority so that the OS will trust ours
mkcert -install

# Generate a certificate for the localhost domain
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```
- Create an SSL certificate


### Run the development server:
```bash
cd reciply
runserver_plus 8000 --settings=config.settings --configuration=Settings --cert-file=cert.pem --key-file=key.pem
```
