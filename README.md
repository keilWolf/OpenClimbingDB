# OpenClimbingDB

OpenClimbingDB is a hobby project for exposing an open database,
so it can log my routes i climbed.

The software is written in python with the power of django, to
learn about that. Never used it before.

The basic data is not feeded manualy. It is crawled from different
existing websites. I united them, so that i don't have to log in 
each in seperate for distributed logging.

Thanks to all website providers for there informations.

Crawling for this project is not intented to be in context of (D)DOS.
I will try not to make too many requests to your servers so that the 
running operation is not affected.

## Getting Started

### Prepare

```bash
git checkout <path to git>
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Migrations

If you change something for the database like the model or co. You have to create some migration file with `makemigrations` and `migrate` afterwards.

```bash
python manage.py makemigrations
```

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

### Update Entity Relation Diagram (ERD) of current database implementation

```bash
python manage.py graph_models ocdb -o ./docs/ocdb_db.png
```

## Remove Data From DB

!!! ATTENTION !!!
!!! Example Will Remove All Sector Entries !!

```bash
python manage.py dbshell
...
DELETE FROM ocdb_sector;
```

## Crawling

see ./crawler/README.md

## About the author

Wolfram Keil
