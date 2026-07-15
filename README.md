##Box Selection System

A Django-based system that recommends the most suitable shipping box for
an ecommerce order, based on the combined dimensions and weight of the
products in that order.

**Live demo:** `https://box-recommendation-system-6.onrender.com/api/recommend-box/` 
**API endpoint:** `POST https://box-recommendation-system-6.onrender.com/api/recommend-box/`

---

## How it works

1. A client sends a list of products (length, width, height, weight) in
   the request body.
2. The system computes the total volume and total weight of the order.
3. It compares the order against every box in the `Box` table and finds
   boxes that satisfy:
   - Each individual product's dimensions fit within the box's internal
     dimensions (per-dimension check, not just total volume).
   - Total order weight ≤ box's maximum weight capacity.
   - Total order volume ≤ box's internal volume.
4. Among all boxes that fit, the cheapest one is returned. Ties are
   broken by smallest internal volume.
5. If no box fits, the API returns a clear "no suitable box" response
   instead of failing silently.

**Units:** all dimensions are in **cm**, weight in **kg**, cost in
**`<your currency, e.g. INR>`**.

**Known simplification:** this uses a per-product dimension + aggregate
volume/weight check, not true 3D bin-packing. A set of products whose
individual dimensions fit but whose combined shapes wouldn't physically
pack together in reality could still be recommended a box. This is
documented as an accepted limitation given the assignment's scope — see
`AI_USAGE.md` for more on this design decision.

---

## Tech stack

- Django `4.2.11`
- Django REST Framework `3.17.1`
- PostgreSQL

---

## Project structure

```
box_recommender/
│
├── .env                     # Local environment variables (database keys, secret keys, etc.)
├── .gitignore               # Specifying files and folders untracked by Git (e.g., .venv, *.pyc)
├── db.sqlite3               # Local SQLite database (if used for development)
├── manage.py                # Django CLI utility for administrative tasks
├── requirements.txt         # Project dependencies
│
├── box_recommender/         # Project configuration directory
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── asgi.py              # ASGI configuration for asynchronous web servers
│   ├── settings.py          # Main settings and configuration for the Django project
│   ├── test_settings.py     # Configurations used specifically for running tests
│   ├── urls.py              # Root URL routing definitions
│   └── wsgi.py              # WSGI configuration for deployment
│
└── boxes/                   # Core Django application for the box recommendation system
    ├── __init__.py          # Marks the application directory as a Python package
    ├── admin.py             # Admin panel registrations for the Box model
    ├── apps.py              # Application configuration
    ├── models.py            # Database schemas/models (e.g., Box model definitions)
    ├── serializers.py       # DRF Serializers for request/response validation (RecommendBoxRequestSerializer)
    ├── tests.py             # Test cases for views, models, and recommendation logic
    ├── urls.py              # App-specific URL routes (e.g., /api/recommend-box/)
    ├── views.py             # Core views/API endpoints (e.g., RecommendBoxView)
    └── migrations/          # Database migrations history
        ├── __init__.py
        └── 0001_initial.py  # Initial migration schema for the Box table

```

---

## Running locally

### Prerequisites

- Python 3.10+
- PostgreSQL installed and running locally
  ([macOS](https://www.postgresql.org/download/macosx/) /
  [Ubuntu](https://www.postgresql.org/download/linux/ubuntu/) /
  [Windows](https://www.postgresql.org/download/windows/))

### 1. Clone the repo

```bash
git clone https://github.com/adarshnema2025/Box-Recommendation-System.git
cd Box-Recommendation System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the Postgres database

```bash
psql postgres
```
```sql
CREATE DATABASE tradexadb;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE tradexadb TO postgres;
\q
```

### 5. Configure environment variables

Copy the example env file and fill in your local Postgres credentials:

```bash
cp .env.example .env
```

`.env.example`:
```
DB_NAME=tradexadb or  whatever you name it
DB_USER=postgres or  whatever you put in
DB_PASSWORD=password or whatever you put in
DB_HOST=localhost
DB_PORT=5432

```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Load sample box data (10 boxes)

Raw SQL :

Connect to your database:

```bash
psql -U postgres -d tradexadb -h localhost
```

Then run:

```sql
INSERT INTO box (id, serial_no, name, internal_length, internal_width, internal_height, max_weight_capacity, cost)
VALUES
(1,  'BOX-001', 'Extra Small',     10, 10, 10, 1,  15),
(2,  'BOX-002', 'Small Mailer',    15, 10, 5,  2,  18),
(3,  'BOX-003', 'Small Cube',      20, 20, 20, 5,  28),
(4,  'BOX-004', 'Medium Standard', 30, 25, 20, 8,  40),
(5,  'BOX-005', 'Medium Flat',     40, 30, 10, 6,  35),
(6,  'BOX-006', 'Medium Cube',     35, 35, 35, 12, 55),
(7,  'BOX-007', 'Large Standard',  50, 40, 30, 15, 70),
(8,  'BOX-008', 'Large Wide',      60, 45, 25, 18, 80),
(9,  'BOX-009', 'Extra Large',     70, 50, 40, 25, 110),
(10, 'BOX-010', 'Heavy Duty',      45, 45, 45, 30, 95);

-- Reset the auto-increment sequence so future Django-created rows
-- don't collide with these manually inserted IDs
SELECT setval(pg_get_serial_sequence('box', 'id'), (SELECT MAX(id) FROM box));
```

> Table name follows Django's convention `<app_label>_<model_name>` in
> lowercase (`box` here) — adjust if your app or model name
> differs. Run `python manage.py migrate` (step 6) before this step so
> the table exists.

### 8. Run the server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/recommend-box/`.

---

## API usage

### Request

```
POST /api/recommend-box/
Content-Type: application/json
```

```json
{
  "products": [
    {"length": 12, "width": 8, "height": 5, "weight": 1.5},
    {"length": 10, "width": 10, "height": 10, "weight": 2}
  ]
}
```

### Response — box found

```json
{
  "recommended_box": {
    "serial_no": "BOX-004",
    "name": "Medium Standard",
    "internal_length": 30,
    "internal_width": 25,
    "internal_height": 20,
    "max_weight_capacity": 8,
    "cost": 40
  },
  "total_weight": 3.5,
  "total_volume": 1480
}
```

### Response — no box fits

```json
{
  "recommended_box": null,
  "message": "No suitable box found for the given products."
}
```

---


---

## Deployment (Render)

This project is deployed on [Render](https://render.com) as a Web
Service, with a Render-managed PostgreSQL instance.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn box_recommender.wsgi:application`
- **Environment variables set on Render:** `DATABASE_URL` (auto-provided
  by Render's Postgres add-on), `SECRET_KEY`, `DEBUG=False`,
  

---

## Other files in this repo

