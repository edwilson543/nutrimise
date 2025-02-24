### AI and linear optimisation powered meal planning application

#### Features
- Extract recipes from images of cookbooks, recipe cards or even handwritten recipes
- Create meal plans that are optimised by, and or satisfy constraints on:
    - Semantic similarity to a prompt
    - Intake of micro and macro nutrients per meal, day or week
    - Number of different ingredients used in the plan
    - Number of different recipes used in the plan
- Get the shopping list for your meal plan

---

### System requirements:
- Python 3.11
- postgres 15.1
- uv

---

### Installation:

```bash
uv venv --python 3.12
source .venv/bin/activate
make install
```

Verify the installation:
```bash
make local_ci
```

And then run the development server:
```bash
make server
```
