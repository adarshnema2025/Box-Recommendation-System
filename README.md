# AI-Assisted Box Selection System

A Django-based system that recommends the most suitable shipping box for
an ecommerce order, based on the combined dimensions and weight of the
products in that order.

**Live demo:** `<your-render-url>` (e.g. `https://box-selector.onrender.com`)
**API endpoint:** `POST <your-render-url>/api/recommend-box/`

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

- Python `<your version, e.g. 3.11>`
- Django `<your version>`
- Django REST Framework `<if used>`
- PostgreSQL

---

## Project structure

```
<update to match your actual layout, e.g.>
box_selector/
├── boxes/
│   ├── models.py          # Box model
│   ├── views.py           # recommend-box API view
│   ├── serializers.py     # request/response validation
│   ├── logic.py           # box selection algorithm
│   ├── fixtures/
│   │   └── boxes.json     # 10 sample boxes
│   └── tests.py
├── box_selector/
│   ├── settings.py
│   └── urls.py
├── requirements.txt
├── manage.py
├── README.md
├── AI_USAGE.md
├── TEST_OUTPUT.md
└── chat_transcript.<md/pdf>
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
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv
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
CREATE DATABASE boxdb;
CREATE USER boxuser WITH PASSWORD 'boxpass';
GRANT ALL PRIVILEGES ON DATABASE boxdb TO boxuser;
\q
```

### 5. Configure environment variables

Copy the example env file and fill in your local Postgres credentials:

```bash
cp .env.example .env
```

`.env.example`:
```
DB_NAME=boxdb
DB_USER=boxuser
DB_PASSWORD=boxpass
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=<your-secret-key>
DEBUG=True
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Load sample box data (10 boxes)

**Option A — Django fixture (recommended):**

```bash
python manage.py loaddata boxes.json
```

**Option B — raw SQL (if you prefer inserting directly via psql):**

Connect to your database:

```bash
psql -U boxuser -d boxdb -h localhost
```

Then run:

```sql
INSERT INTO boxes_box (id, serial_no, name, internal_length, internal_width, internal_height, max_weight_capacity, cost)
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
SELECT setval(pg_get_serial_sequence('boxes_box', 'id'), (SELECT MAX(id) FROM boxes_box));
```

> Table name follows Django's convention `<app_label>_<model_name>` in
> lowercase (`boxes_box` here) — adjust if your app or model name
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

## Running tests

```bash
python manage.py test
```

Test run output is captured in [`TEST_OUTPUT.md`](./TEST_OUTPUT.md)
(or see the GitHub Actions run: `<link if using CI>`).

---

## Deployment (Render)

This project is deployed on [Render](https://render.com) as a Web
Service, with a Render-managed PostgreSQL instance.

- **Build command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata boxes.json`
- **Start command:** `gunicorn box_selector.wsgi:application`
- **Environment variables set on Render:** `DATABASE_URL` (auto-provided
  by Render's Postgres add-on), `SECRET_KEY`, `DEBUG=False`,
  `ALLOWED_HOSTS=<your-render-domain>`

---

## Other files in this repo

- [`AI_USAGE.md`](./AI_USAGE.md) — AI tools used, prompts, what was
  accepted/rejected, mistakes found, and how the final code was verified.
- `chat_transcript.<ext>` — exported chat transcript (written without AI
  assistance, as required).
- `LEARNINGS.md` — reflection on what was learned in this assignment
  (written without AI assistance, as required).
- [`TEST_OUTPUT.md`](./TEST_OUTPUT.md) — terminal output from the test
  run.
