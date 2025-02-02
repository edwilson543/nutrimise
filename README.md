### Web app for optimising meal plans

#### Features
- Generate meal plans for any schedule (e.g. day, week, month) from your library of recipes
- Set requirements for each meal plan, including:
  - Minimum or maximum quantity of micro and macro nutrients
  - Minimum or maximum number of different ingredients utilised in different categories (e.g. vegetables)
- Optimise the meal plans across various objectives:
  - Nutrition
  - Variation

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
