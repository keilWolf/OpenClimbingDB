from django.db.migrations.operations.base import Operation
from django.core.management import call_command


class LoadFixture(Operation):
    reduces_to_sql = False
    reversible = True

    def __init__(self, model, *fixtures):
        self.model = model
        self.fixtures = fixtures

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        for fixture in self.fixtures:
            call_command("loaddata", fixture, app_label=app_label)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return "Load Fixture Operation"
