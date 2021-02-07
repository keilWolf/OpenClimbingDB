"""Script to transform countries file to django fixture format."""
import json
import abc


class Fixture(abc.ABC):
    def __init__(self, name, parent, grandparent):
        self.name = name
        self.parent = parent
        self.grandparent = grandparent
        self.props = {}

    def add_prop(self, key, value):
        self.props[key] = value

    def to_fixture(self):
        """Convert given iterable to dict for json transformation.

        Desired Format for djangod
            {
                "id" : None,
                "model" : "ocdb.Sector",
                "fields" : {
                    "name" : <mandatory>
                    "fk_sector" : <optional> *
                }
            }

            *e.g. not for elements with no more parents like continents
        """
        data = {}
        data["id"] = None
        data["model"] = "ocdb." + self.__class__.__name__
        data["fields"] = {"name": self.name}

        if (self.parent is not None) and (self.grandparent is not None):
            data["fields"]["fk_sector"] = (self.parent, self.grandparent)

        for prop in self.props:
            data["fields"][prop] = self.props[prop]

        return data


class Sector(Fixture):
    pass


class Route(Fixture):
    pass


if __name__ == "__main__":

    areas = dict()
    sectors = dict()
    summits = dict()
    routes = dict()

    with open("./germany-testdata.jsonl", "r") as f:
        for line in f:
            data = json.loads(line)

            if "area" in data:
                area = data["area"]
                area_id = data["area_id"]
                areas[area_id] = Sector(area, "Germany", "Western Europe")

            if "sector" in data:
                sector_name = data["sector"]
                sector_id = data["db_id"]
                area_name = areas[data["area_id"]].name
                sectors[sector_id] = Sector(sector_name, area_name, "Germany")

            if "summit" in data:
                summit_name = data["summit"]
                summit_id = data["db_id"]
                sector_id = data["sector_id"]
                sector_name = sectors[sector_id].name
                area_name = sectors[sector_id].parent
                summits[summit_id] = Sector(summit_name, sector_name, area_name)

            if "lat" in data:
                lat = data["lat"]
                lon = data["lon"]
                summit = summits[data["summit_db_id"]]
                summit.add_prop("lat", lat)
                summit.add_prop("lon", lon)

            if "route_name" in data:
                route_name = data["route_name"]
                route_id = data["route_id"]
                summit_id = data["summit_id"]
                summit_name = summits[summit_id].name
                sector_name = summits[summit_id].parent
                routes[route_id] = Route(route_name, summit_name, sector_name)

    print(list(routes.values())[0].to_fixture())

    """
    with open("../../ocdb/fixtures/db_sandstein_fixture.json", "w") as f_out:
        json.dump(out, f_out, indent=True)
    """
