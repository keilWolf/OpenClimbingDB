# Basic Regions

## Data Source

./countries.json
https://datahub.io/core/country-codes

## Generate django fixture for import

```bash
python create_django_fixture.py
```

## Import data into django app

```bash
python manage.py loaddata ./ocdb/fixtures/basic_regions_fixture.json
```

## Remove Sectors

!!! ATTENTION !!!
!!! Will Remove All Sector Entries !!

```bash
python manage.py dbshell
...
DELETE FROM ocdb_sector;
```