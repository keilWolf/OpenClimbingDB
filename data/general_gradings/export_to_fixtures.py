import json
import os
from pathlib import Path
import pandas

FIXTURES_OUT = "../../ocdb/fixtures/"


class GradeSystemTypeCollection:
    def __init__(self):
        self.grade_system_types = []
        self.count = 0

    def add(self, name):
        self.count += 1
        self.grade_system_types.append(
            {
                "pk": self.count,
                "model": "ocdb.GradeSystemType",
                "fields": {"name": name},
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}grade_system_type_fixture.json", "w") as f:
            json.dump(self.grade_system_types, f, indent=4)


class GradeSystemCollection:
    def __init__(self):
        self.grade_system = []
        self.count = 0

    def add(self, name, fk_grade_system_type):
        self.count += 1
        self.grade_system.append(
            {
                "pk": self.count,
                "model": "ocdb.GradeSystem",
                "fields": {"name": name, "fk_grade_system_type": fk_grade_system_type},
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}grade_system_fixture.json", "w") as f:
            json.dump(self.grade_system, f, indent=4)


class GradeCollection:
    def __init__(self):
        self.grades = []
        self.count = 0

    def add(self, name, weight, fk_grade_system):
        self.count += 1
        self.grades.append(
            {
                "pk": self.count,
                "model": "ocdb.Grade",
                "fields": {
                    "name": name,
                    "weight": weight,
                    "fk_grade_system": fk_grade_system,
                },
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}grade_fixture.json", "w") as f:
            json.dump(self.grades, f, indent=4)


def main():
    path = Path(__file__)
    files = os.listdir(path.parent)

    grade_system_types = GradeSystemTypeCollection()
    grade_systems = GradeSystemCollection()
    grade_collection = GradeCollection()

    for file in files:
        if file.endswith(".csv"):
            grade_system_types.add(Path(file).stem.capitalize())
            data = pandas.read_csv(file)
            for col_name in data.columns[1:]:
                col = data[col_name]
                grade_systems.add(col_name, grade_system_types.count)
                for weight, row in enumerate(col):
                    if pandas.notna(row):
                        grade_collection.add(row, weight, grade_systems.count)

    grade_system_types.export()
    grade_systems.export()
    grade_collection.export()


if __name__ == "__main__":
    main()
