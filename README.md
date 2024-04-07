### Backend for the [reciply mobile app](https://github.com/edwilson543/reciply-mobile)

- Django and Django Rest Framework for the API used by the app
- Django Rest Knox for token authentication
- Postgres for the database
- Plugin S3 integration for storing images

---

### System requirements:
- Python 3.11
- postgres 15.1
- mkcert 1.4.4 (optional)

---

### Installation:

```bash
python3.11 -m venv venv
source venv/bin/activate
make install
```

---

### Run the development server:
With HTTP:
```bash
make server
```

With HTTPS:
```bash
make server_https
```

---
