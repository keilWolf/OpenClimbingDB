# DB Sandstein Import

## Data Source

crawled json-lines from 

https://github.com/keilWolf/ClimbingCrawler"

## Generate django fixture for import

```bash
python create_django_fixture.py
```

## Import data into django app

```bash
python manage.py loaddata <path to fixture>fixture.json
```
