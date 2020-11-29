# OpenClimbingDB

OpenClimbingDB is a hobby project for exposing an open database
for purposes of climbing like logging the routes that i climbed.

The software is written in python with the power of django, to
learn about that. Never used it before.

## Getting Started

### Prepare

```bash
git checkout <path to git>
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Migrations

```bash
python manage.py migrate
```

### Superuser

```bash
python manage.py createsuperuser --email admin@example.com --username admin
```

### Start

```bash
python manage.py runserver
```

### Update ERD - Diagramm of current database implementation

```bash
python manage.py graph_models ocdb -o ./docs/ocdb_db.png
```

## About the author

Me
