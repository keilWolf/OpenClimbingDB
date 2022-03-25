"""Scrapy Spider to crawl data from http://db-sandsteinklettern.gipfelbuch.de."""
import json
import logging
from datetime import datetime

import scrapy
from crawler.climbing_crawler.db_sandstein.parser import (
    GradeMatch,
    GradeParser,
)
from ocdb.models import AscentStyle, Grade, GradeSystem, Route, RouteGrades, Sector

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
    "Großbritannien": "UK",
    "Finnland": "Finland",
    "Schweden": "Sweden",
}


def meta_to_str(meta):
    """Meta 2 str.

    Arguments:
        meta(dict) part of the scrapy spider response
    """
    c = meta.get("country", "")
    a = meta.get("area", "")
    s = meta.get("sector", "")
    return f"{c}:{a}:{s}"


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
        for entry in json_res[5:]:
            country_name = entry["land"]
            print("-" * 50)
            print(f"process ... {country_name}")
            print("-" * 50)
            if country_name not in hook_in_countries:
                raise ValueError(f"Check if {country_name} is in hook_in_country list.")
            country = Sector.objects.get(name=hook_in_countries[country_name])
            response.meta["country"] = country
            yield response.follow(
                get_area_url(country_name), self.parse_area, meta=response.meta
            )
            break

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
            area, _ = Sector.objects.get_or_create(
                name=entry["gebiet"], fk_sector=response.meta["country"]
            )
            area.source = response.url
            area.save()

            response.meta["area"] = area
            yield response.follow(
                get_sector_url(entry["gebiet_ID"]),
                self.parse_sector,
                meta=response.meta,
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
        if json_res is not None:
            for entry in json_res:
                sector, _ = Sector.objects.get_or_create(
                    name=entry["sektorname_d"], fk_sector=response.meta["area"]
                )
                sector.source = response.url
                sector.name_alt = entry["sektorname_cz"]
                sector.sub_id_in_parent_sector = entry["sektornr"]
                sector.save()

                response.meta["sector"] = sector
                response.meta["db_sandstein_id"] = entry["sektor_ID"]
                yield response.follow(
                    get_summit_url(entry["sektor_ID"]),
                    self.parse_summit,
                    meta=response.meta,
                )
        else:
            logging.info(f"No entries available for {meta_to_str(response.meta)}")

    def parse_summit(self, response):
        """Parse summit from response.

        Example: Teufelsturm
        """
        json_res = json.loads(response.body)
        if json_res is not None:
            for entry in json_res:
                summit, _ = Sector.objects.get_or_create(
                    name=entry["gipfelname_d"], fk_sector=response.meta["sector"]
                )
                summit.source = response.url
                summit.name_alt = entry["gipfelname_cz"]
                summit.sub_id_in_parent_sector = entry["gipfelnr"]
                summit.latitude = entry["ngrd"]
                summit.longitude = entry["vgrd"]
                summit.save()

                response.meta["summit"] = summit
                response.meta["db_sandstein_id"] = entry["gipfel_ID"]
                response.meta["sector"] = response.meta["sector"]

                sector_id = response.meta["db_sandstein_id"]
                yield response.follow(
                    get_routes_url(sector_id),
                    self.parse_routes,
                    meta=response.meta,
                )
        else:
            logging.info(f"No entries available for {meta_to_str(response.meta)}")

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
                "wegnr": "6",http://db-sandsteinklettern.gipfelbuch.de/jsonwege.php?app=yacguide&sektorid=326
            }
        """  # noqa: E501

        json_res = json.loads(response.body)
        if json_res is not None:
            for entry in json_res:
                route, _ = Route.objects.get_or_create(
                    name=entry["wegname_d"], fk_sector=response.meta["summit"]
                )
                route.source = response.url
                route.name_alt = entry["wegname_cz"]
                route.description = entry["wegbeschr_d"]
                route.description_alt = entry["wegbeschr_cz"]
                route.protection = f"Ringzahl: {entry['ringzahl']}"

                date = entry["erstbegdatum"]
                if date and date != "0000-00-00":
                    route.first_ascent_date = datetime.strptime(date, "%Y-%m-%d").date()
                route.first_ascent_persons = ",".join(
                    (entry["erstbegvorstieg"], entry["erstbegnachstieg"])
                )
                route.save()

                raw_diffs = entry["schwierigkeit"]
                if len(raw_diffs) > 0:
                    try:
                        diffs = GradeParser().parse(raw_diffs)
                        for diff in diffs:
                            try:
                                save_route_grade_item(diff, route)
                            except Exception as e:
                                print("-" * 50)
                                print(raw_diffs)
                                print(diff)
                                raise e
                    except ValueError as e:
                        print("+" * 50)
                        print(raw_diffs)
                        raise e
                    except LookupError:
                        logging.warning("Temporary Exceptions.")
                else:
                    logging.warning("No grades available.")


def save_route_grade_item(diff: GradeMatch, route):
    """Get RouteGradeItems from parsed difficulties."""
    created = False
    gs = GradeSystem.objects.get(name=diff.gs.value)
    ascent_style = AscentStyle.objects.get(name=diff.diff_type.value)
    grade = Grade.objects.get(name=diff.grade_str, fk_grade_system=gs)
    route_grade, created = RouteGrades.objects.get_or_create(
        fk_route=route, fk_ascent_style=ascent_style, fk_grade=grade
    )
    if created:
        route_grade.save()
