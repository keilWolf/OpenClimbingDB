import json
import os
from pathlib import Path
import pandas


FIXTURES_OUT = "../../ocdb/fixtures/"


def to_upper_camelcase(lower_underscore: str):
    """Convert underscore naming to upper camelcase.

    Example:
        rock_type --> RockType
    """

    splits = lower_underscore.split("_")
    splits = [split.capitalize() for split in splits]
    return "".join(splits)


class SimpleCollection:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.values = []
        self.count = 0

    def add(self, name):
        self.count += 1
        self.values.append(
            {
                "pk": self.count,
                "model": f"ocdb.{to_upper_camelcase(self.collection_name)}",
                "fields": {"name": name},
            }
        )

    def export(self):
        with open(f"{FIXTURES_OUT}/{self.collection_name}_fixture.json", "w") as f:
            json.dump(self.values, f, indent=4)


def main():
    path = Path(__file__)
    files = os.listdir(path.parent)

    for file in files:
        if file.endswith(".csv"):
            print(f"Process file [{file}]")
            file_name = Path(file).stem
            sc = SimpleCollection(file_name)
            data = pandas.read_csv(file, header=None)
            for row in data[0]:
                sc.add(row)
            sc.export()


if __name__ == "__main__":
    main()
