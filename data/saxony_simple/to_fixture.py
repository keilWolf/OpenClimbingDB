import pandas
import json
from pathlib import Path

FIXTURES_OUT = "../../ocdb/fixtures/"


class AreaCollection:
    def __init__(self):
        self.areas = {}
        self.count = 0
        self.out = []

    def add(self, name):
        self.count += 1
        self.areas[name] = self.count
        self.out.append(
            {
                "pk": self.count,
                "model": "ocdb.Sector",
                "fields": {"name": name},
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}sector_area_fixture.json", "w") as f:
            json.dump(self.out, f, indent=4, ensure_ascii=False)


class SummitCollection:
    def __init__(self):
        self.out = []
        self.count = 0

    def add(self, name, fk_area):
        self.count += 1
        self.out.append(
            {
                "pk": self.count,
                "model": "ocdb.Sector",
                "fields": {"name": name, "fk_sector": fk_area},
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}sector_summit_fixture.json", "w") as f:
            json.dump(self.out, f, indent=4, ensure_ascii=False)


def export_areas(fp):
    area_collection = AreaCollection()
    areas = pandas.read_csv(fp, header=None)
    for area in areas[0]:
        area_collection.add(area)
    area_collection.export()


def export_summits(fp):
    summit_collection = SummitCollection()
    summits = pandas.read_csv(fp, delimiter=";")
    for i, row in summits.iterrows():
        name = row["Name"]
        fk_id = row["FK_Area"]
        summit_collection.add(name, fk_id)
    summit_collection.export()


def main():
    path = Path(__file__).parent

    export_areas(path.joinpath("areas.csv"))
    export_summits(path.joinpath("summits.csv"))


if __name__ == "__main__":
    main()
