### Web app for generating meal plans

#### Features
- Manage recipes and meal plans using a slick UI (the Django admin but purple)
- Generate meal plans using a linear optimiser 
- Impose various constraints on your meal plan:
  - Intake of micro and macro nutrients per meal / day / week etc.
  - Number of different ingredients used in the plan
  - Number of different recipes used in the plan
- Optimise meal plans for various objectives:
  - Randomness
  - Maximise or minimise the intake of certain nutrients
  - Maximise or minimise the number of different ingredients used
  - Maximise semantic matching between a prompt and the chosen recipes
- Semantic search for recipes using word embeddings

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
