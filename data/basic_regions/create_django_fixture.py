"""Script to transform countries file to django fixture format."""
import json


def arr_to_json_fixturen(array):
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
    data["model"] = "ocdb.Sector"
    data["fields"] = {
        "name": array[0],
    }

    parent = array[1:]
    if parent != (None, None):
        data["fields"]["fk_sector"] = parent

    return data


if __name__ == "__main__":

    regions = set()
    sub_regions = set()
    intermediate_regions = set()
    countries = set()

    with open("./countries.json", "r") as f:
        data = json.load(f)
        for entry in data:
            region = entry["Region Name"]
            sub_region = entry["Sub-region Name"]
            intermediate_region = entry["Intermediate Region Name"]
            country = entry["CLDR display name"]

            next_parent = (None, None)

            if region is not None:
                regions.add((region, None, None))
                next_parent = (region, None)

            if sub_region is not None:
                sub_regions.add((sub_region, region, None))
                next_parent = (sub_region, region)

            if intermediate_region is not None:
                intermediate_regions.add((intermediate_region, sub_region, region))
                next_parent = (intermediate_region, sub_region)

            countries.add((country,) + next_parent)

    out = []
    out = out + ([arr_to_json_fixturen(r) for r in regions])
    out = out + ([arr_to_json_fixturen(sr) for sr in sub_regions])
    out = out + ([arr_to_json_fixturen(ir) for ir in intermediate_regions])
    out = out + ([arr_to_json_fixturen(c) for c in countries])

    with open("../../ocdb/fixtures/basic_regions_fixture.json", "w") as f_out:
        json.dump(out, f_out, indent=True)
