## Backend for the reciply mobile app

---

## Setup:
### System requirements:
- Python 3.11

### Installation:
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements/app-requirements.txt
cd reciply
python manage.py migrate
```

### Running:
```bash
cd reciply
python manage.py runserver 8000
```
