from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import List


FIXTURES_OUT = "../../ocdb/fixtures/"


@dataclass
class Grade:
    name: str
    weight: int

    def as_django_fixture(self, pk: int, fk: int):
        return {
            "pk": pk,
            "model": "ocdb.Grade",
            "fields": {
                "name": self.name,
                "weight": self.weight,
                "fk_grade_system": fk,
            },
        }


@dataclass
class GradeSystem:
    name: str
    grades: List[Grade]

    def as_django_fixture(self, pk: int, fk: int):
        return {
            "pk": pk,
            "model": "ocdb.GradeSystem",
            "fields": {"name": self.name, "fk_grade_system_type": fk},
        }


@dataclass
class GradeSystemType:
    name: str
    grade_systems: List[GradeSystem]

    def as_django_fixture(self, pk: int):
        return {
            "pk": pk,
            "model": "ocdb.GradeSystemType",
            "fields": {"name": self.name},
        }


def export(grade_system_types: List[GradeSystemType]):

    types = []
    systems = []
    grades = []

    pk_type = 0
    pk_system = 0
    pk_grade = 0

    for gst in grade_system_types:
        pk_type += 1
        types.append(gst.as_django_fixture(pk_type))

        for system in gst.grade_systems:
            pk_system += 1
            systems.append(system.as_django_fixture(pk_system, pk_type))

            for grade in system.grades:
                pk_grade += 1
                grades.append(grade.as_django_fixture(pk_grade, pk_system))

    with open(f"{FIXTURES_OUT}grade_system_type_fixture.json", "w") as f:
        json.dump(types, f, indent=4)

    with open(f"{FIXTURES_OUT}grade_system_fixture.json", "w") as f:
        json.dump(systems, f, indent=4)

    with open(f"{FIXTURES_OUT}grade_fixture.json", "w") as f:
        json.dump(grades, f, indent=4)


def main():
    path = Path(__file__)
    files = os.listdir(path.parent)

    grade_system_types = []

    for file in files:
        if file.endswith(".csv"):
            grade_system_type_name = Path(file).stem.capitalize()
            grade_system_type = GradeSystemType(grade_system_type_name, [])
            grade_system_types.append(grade_system_type)

            with open(file, "r") as data:
                # read header -> grade system names
                grade_system_names = data.readline().split(",")[1:]
                for gsn in grade_system_names:
                    grade_system_name = gsn.replace("\n", "")
                    grade_system = GradeSystem(grade_system_name, [])
                    grade_system_type.grade_systems.append(grade_system)

                # read rows
                line = data.readline()
                while line:
                    row = line.split(",")
                    weight = int(row[0])
                    for i, grade in enumerate(row[1:]):
                        grade = grade.replace("\n", "")
                        if not grade == "":
                            grade = Grade(grade, weight)
                            grade_system_type.grade_systems[i].grades.append(grade)
                    line = data.readline()

    export(grade_system_types)


if __name__ == "__main__":
    main()
