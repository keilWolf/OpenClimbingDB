init:
	./venv/bin/python manage.py migrate
	./venv/bin/python manage.py loaddata ./ocdb/fixtures/basic_regions_fixture.json
