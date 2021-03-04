"""Scrapy Spider to crawl data from http://db-sandsteinklettern.gipfelbuch.de."""
import json
from datetime import datetime

import scrapy

from crawler.climbing_crawler.items import SectorItem, RouteItem, RouteGradeItem
from crawler.climbing_crawler.db_sandstein_util import parse_difficulties
from ocdb.models import Sector, Grade, AscentStyle, GradeSystem

BASE_URL = "http://db-sandsteinklettern.gipfelbuch.de"

# Countries alreay existing in the db
# Dict will map to the correct existing db entry

hook_in_countries = {
    "Bulgarien": "Bulgaria",
    "Deutschland": "Germany",
    "Griechenland": "Greece",
    "Namibia": "Namibia",
    "Polen": "Poland",
    "Tschechische Republik": "Czechia",
    "Türkei": "Turkey",
    "Jordanien": "Jordan",
    "Italien": "Italy",
    "Spanien": "Spain",
    "China": "China",
    "Russland": "Russia",
    "Portugal": "Portugal",
    "Österreich": "Austria",
    "Schweiz": "Switzerland",
    "Frankreich": "France",
    "Slowakei": "Slovakia",
    "Großbritannien": ["UK"],
}


def get_area_url(landname):
    """Use jsongebiet.php API."""
    return f"{BASE_URL}/jsongebiet.php?app=yacguide&land={landname}"


def get_sector_url(area_id: int):
    """Use jsonteilgebiet.php API."""
    return f"{BASE_URL}/jsonteilgebiet.php?app=yacguide&gebietid={area_id}"


def get_summit_url(sector_id: int):
    """Use jsongipfel.php API."""
    return f"{BASE_URL}/jsongipfel.php?app=yacguide&sektorid={sector_id}"


def get_routes_url(sector_id: int):
    """Use jsonwege.php API."""
    return f"{BASE_URL}/jsonwege.php?app=yacguide&sektorid={sector_id}"


class DBSandsteinJsonSpider(scrapy.Spider):
    name = "DBSandsteinJsonSpider"
    start_urls = [f"{BASE_URL}/jsonland.php?app=yacguide"]

    def parse(self, response):
        """Parse country from response and find existing entry from db.

        Example:
            {
                "land": "Bulgarien",
                "ISO3166": "bg",
                "KFZ": "BG"
            }
        """
        json_res = json.loads(response.body)
        for entry in json_res:
            country_name = entry["land"]
            country = Sector.objects.get(name=hook_in_countries[country_name])
            meta = {"country": country}
            yield response.follow(
                get_area_url(country_name), self.parse_area, meta=meta
            )

    def parse_area(self, response):
        """Parse area from response.

        Example:
            {
                "gebiet_ID": "21",
                "gebiet": "Erzgebirge",
                "land": "Deutschland",
                "sprache2": "deutsch",
                "gdefaultanzeige": "alle",
                "schwskala": "0",
            }
        """
        json_res = json.loads(response.body)
        for entry in json_res:
            item = SectorItem()
            item["name"] = entry["gebiet"]
            item["fk_sector"] = response.meta["country"]
            item["source"] = response.url
            yield item

            area = item.django_model.objects.get(**item)
            meta = {"area": area}
            yield response.follow(
                get_sector_url(entry["gebiet_ID"]), self.parse_sector, meta=meta
            )

    def parse_sector(self, response):
        """Parse sector from response.

        Example:
            {
                "sektor_ID": "123",
                "gebietid": "19",
                "sektornr": "6",
                "sektorname_d": "Affensteine",
                "sektorname_cz": "",
            }
        """
        json_res = json.loads(response.body)
        for entry in json_res:
            item = SectorItem()
            item["fk_sector"] = response.meta["area"]
            item["source"] = response.url
            item["name"] = entry["sektorname_d"]
            item["name_alt"] = entry["sektorname_cz"]
            item["sub_id_in_parent_sector"] = entry["sektornr"]
            yield item

            sector = item.django_model.objects.get(**item)
            meta = {"sector": sector, "db_sandstein_id": entry["sektor_ID"]}
            yield response.follow(
                get_summit_url(entry["sektor_ID"]), self.parse_summit, meta=meta
            )

    def parse_summit(self, response):
        """Parse summit from response.

        Example: Teufelsturm
        """
        json_res = json.loads(response.body)
        for entry in json_res:
            item = SectorItem()
            item["fk_sector"] = response.meta["sector"]
            item["source"] = response.url
            item["name"] = entry["gipfelname_d"]
            item["name_alt"] = entry["gipfelname_cz"]
            item["sub_id_in_parent_sector"] = entry["gipfelnr"]
            item["latitude"] = entry["ngrd"]
            item["longitude"] = entry["vgrd"]
            yield item

            summit = item.django_model.objects.get(**item)
            meta = {
                "summit": summit,
                "db_sandstein_id": entry["gipfel_ID"],
                "sector": response.meta["sector"],
            }
            sector_id = response.meta["db_sandstein_id"]
            yield response.follow(
                get_routes_url(sector_id),
                self.parse_routes,
                meta=meta,
            )

    def parse_routes(self, response):
        """Parse routes from response.

        Example:
            {
                "weg_ID": "4686",
                "gipfelid": "4189",
                "schwierigkeit": "VIIb",
                "erstbegvorstieg": "Heinz Schröder",
                "erstbegnachstieg": "S.Herschel",
                "erstbegdatum": "1953-08-24",
                "ringzahl": "2",
                "wegbeschr_d": "
                    Rechts von Block in der Talseite rechtsh.(nR) zur
                    Südkante. Rechts der Kante leicht überh.Wand (nR),
                    oben etwas rechtsh. zu Abs. Teils überh. Kante z.G.",
                "wegbeschr_cz": "",
                "kletterei": "",
                "wegname_d": "*Südkante",
                "wegname_cz": "",
                "wegstatus": "1",
                "wegnr": "6",
            }
        """

        json_res = json.loads(response.body)
        for entry in json_res:
            print(json.dumps(entry, indent=True))
            route_item = RouteItem()
            route_item["name"] = entry["wegname_d"]
            route_item["name_alt"] = entry["wegname_cz"]
            route_item["description"] = entry["wegbeschr_d"]
            route_item["description_alt"] = entry["wegbeschr_cz"]
            route_item["fk_sector"] = response.meta["summit"]
            route_item["source"] = response.url
            route_item["protection"] = f"Ringzahl: {entry['ringzahl']}"

            date = entry["erstbegdatum"]
            if date:
                route_item["first_ascent_date"] = datetime.strptime(
                    date, "%Y-%m-%d"
                ).date()

            route_item["first_ascent_persons"] = ",".join(
                (entry["erstbegvorstieg"], entry["erstbegnachstieg"])
            )
            yield route_item

            route = route_item.django_model.objects.get(
                name=route_item["name"], fk_sector=route_item["fk_sector"]
            )
            diffs = parse_difficulties(entry["schwierigkeit"])
            for route_grade_item in get_route_grade_items(diffs, route):
                yield route_grade_item


def get_route_grade_items(diffs, route):
    """Get RouteGradeItems from parsed difficulties.

    Returns Generator
    """
    # remove unused difficulty options
    del diffs["danger"]
    del diffs["anstr"]
    for diff_type in diffs:
        if diff_type == "Jump":
            grade_system = GradeSystem.objects.get(name="UIAA")
        else:
            grade_system = GradeSystem.objects.get(name="Saxon")
        diff = diffs[diff_type]
        if diff:
            ascent_style = AscentStyle.objects.get(name=diff_type)
            grade = Grade.objects.get(name=diff, fk_grade_system=grade_system)
            route_grade_item = RouteGradeItem()
            route_grade_item["fk_route"] = route
            route_grade_item["fk_ascent_style"] = ascent_style
            route_grade_item["fk_grade"] = grade
            yield route_grade_item
