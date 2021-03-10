"""Scrapy Spider for url https://www.frankenjura.com."""
import re

import scrapy
from scrapy.http.response.html import HtmlResponse

from crawler.climbing_crawler.items import SectorItem, RouteItem
from ocdb.models import Sector, Orientation, Grade, GradeSystem


class FrankenJuraSpider(scrapy.Spider):
    name = "franken_jura"
    start_urls = ["https://www.frankenjura.com/klettern/panorama"]

    def parse(self, response: HtmlResponse):
        """Parse main page https://www.frankenjura.com/klettern/panorama.

        Region Nordbayern

        Creates main sector 'Frankenjura' and hook it in the database.
        """
        # prepare base item as hook-in
        country = Sector.objects.get(name="Germany")
        base_item = SectorItem()
        base_item["name"] = "Frankenjura"
        base_item["fk_sector"] = country
        yield base_item
        frankenjura = base_item.django_model.objects.get(**base_item)

        regions = response.css('div[class="column"]').css('a[href*="region"]')
        for region in regions:
            meta = {"region_name": region.css("::text").get(), "parent": frankenjura}
            yield response.follow(region, self.parse_region, meta=meta)

    def parse_region(self, response: HtmlResponse):
        """Parse regions.

        Nordbayern -> Frankenjura Nord

        Example: https://www.frankenjura.com/klettern/region/2
        """
        item = SectorItem()
        item["name"] = response.meta["region_name"]
        item["fk_sector"] = response.meta["parent"]
        item["source"] = response.url
        item["description"] = response.css('div[class="location-head"]+p ::text').get()
        yield item

        region = item.django_model.objects.get(**item)

        sub_regions = response.css('div[class="column"]').css('a[href*="region"]')
        for sub_region in sub_regions:
            meta = {"sub_region_name": sub_region.css("::text").get(), "parent": region}
            yield response.follow(sub_region, self.parse_sub_region, meta=meta)

    def parse_sub_region(self, response: HtmlResponse):
        """Parse sub regions.

        ... -> Frankenjura Nord -> Region Wattendorf

        Example: https://www.frankenjura.com/klettern/region/8
        """
        item = SectorItem()
        item["name"] = response.meta["sub_region_name"]
        item["fk_sector"] = response.meta["parent"]
        item["source"] = response.url
        yield item

        sub_region = item.django_model.objects.get(**item)

        walls = response.css("td").css("a")
        for wall in walls:
            meta = {"wall_name": wall.css("::text").get(), "parent": sub_region}
            yield response.follow(wall, self.parse_wall, meta=meta)

    def parse_wall(self, response: HtmlResponse):
        """Parse walls.

        ... -> Region Wattendorf -> Falkenwand

        Example: https://www.frankenjura.com/klettern/poi/21
        """
        item = SectorItem()
        item["name"] = response.meta["wall_name"]
        item["fk_sector"] = response.meta["parent"]
        item["source"] = response.url
        item["internal_rating"] = _parse_stars(response)
        item["max_height_in_m"] = _parse_wall_max_height(response)
        item["rain_protected"] = _parse_rain_protected(response)
        item["child_friendly"] = _parse_child_friendly(response)
        item["description"] = _parse_wall_description(response)
        item["approach"] = _parse_wall_approach(response)
        item["approach_road"] = _parse_wall_approach_road(response)
        item["fk_orientation"] = _parse_orientation(response)
        item["latitude"], item["longitude"] = _parse_lat_lon(response)
        yield item

        wall = item.django_model.objects.get(
            name=item["name"], fk_sector=item["fk_sector"]
        )

        routes = response.css('div[class="poi-link-container"]').css("a")
        for route in routes:
            meta = {"route_name": route.css("::text").get(), "parent": wall}
            yield response.follow(route, self.parse_route, meta=meta)

    def parse_route(self, response: HtmlResponse):
        """Parse route.

        ... -> Falkenwand -> Falken und Bären (7-)

        Example: https://www.frankenjura.com/frankenjura/poi/1659
        """
        item = RouteItem()
        item["name"] = response.meta["route_name"]
        item["fk_sector"] = response.meta["parent"]
        item["source"] = response.url
        item["internal_rating"] = _parse_stars(response)
        item["fk_orientation"] = _parse_orientation(response)
        item["length_in_m"] = _parse_route_length(response)
        item["description"] = _parse_wall_description(response)
        yield item


def _parse_stars(response: HtmlResponse):
    """Parse count of stars given for walls and routes."""
    stars_selector = response.css("img[class*=stars]")
    if stars_selector:
        return int(stars_selector[0].attrib["class"].split("stars")[1])
    else:
        return 0


def _parse_rain_protected(response: HtmlResponse):
    """Parse optional element 'rain protected'."""
    selector = response.css('th:contains("Regensicher") + td ::text')
    if selector:
        value = selector.get()
        return False if value.lower() == "nein" else True
    else:
        return False


def _parse_child_friendly(response: HtmlResponse):
    """Parse optional element 'child friendly'."""
    selector = response.css('th:contains("Kinder") + td ::text')
    if selector:
        value = selector.get()
        return False if "Ungeeignet" in value.lower() else True
    else:
        return False


def _parse_wall_description(response: HtmlResponse):
    """Parse description if available. Otherwise return empty string."""
    return response.css('h4:contains("Beschreibung") + p ::text').get(default="")


def _parse_wall_approach_road(response: HtmlResponse):
    """Parse road approach to wall if available. Otherwise return empty string."""
    return response.css('h4:contains("Zufahrt") + p ::text').get(default="")


def _parse_wall_approach(response: HtmlResponse):
    """Parse approach to wall if available. Otherwise return empty string."""
    return response.css('h4:contains("Zustieg") + p ::text').get(default="")


def _parse_orientation(response: HtmlResponse):
    """Parse Orientation.

    Returns None if not available or is unknown.
    """
    value = response.css('th:contains("Ausrichtung") + td ::text').get()
    if value:
        if value == "unbekannt" or value == "verschieden":
            return None
        fk_value = {
            "Nord": "N",
            "Nordost": "NO",
            "Ost": "O",
            "Südost": "SO",
            "Süd": "S",
            "Südwest": "SW",
            "West": "W",
            "Nordwest": "NW",
        }
        return Orientation.objects.get(name=fk_value[value])
    else:
        return None


def _parse_wall_max_height(response: HtmlResponse):
    """Parse max height of wall.

    Returns 0 if not available.
    """
    return _parse_length(response.css('th:contains("Höhe") + td ::text'))


def _parse_route_length(response: HtmlResponse):
    """Parse route length.

    Returns 0 if not available.
    """
    return _parse_length(response.css('th:contains("Länge") + td ::text'))


def _parse_length(selector):
    """Parse length of route.

    Example:
        - 5 bis 15m
        - bis 10m
        - 8m -> 8
        - 12-15m -> 15
        - None -> 0

    Returns 0 if parsing is not working.
    """
    if selector:
        value = selector.get()
        if value == "unbekannt" or value == "m" or value == "bis":
            return 0
        if "-" in value:
            value = value.split("-")[1]
        if "bis" in value:
            value = value.split(" ")[-1]
        value = value.replace(",", ".")
        length = float(value.split("m")[0])
        return length
    return 0


def _parse_difficulty(response: HtmlResponse):
    """Parse grade of route.

    Field is mandatory.

    Examples:
        - 7+
        - 6-
    """
    value = response.css('th:contains("Schwierigkeit") + td ::text')
    grade_system = GradeSystem.objects.get(name="UIAA")
    grade = Grade.objects.get(name=value, fk_grade_system=grade_system)
    return grade


def _parse_lat_lon(response: HtmlResponse):
    """Parse coordinates.

    Examples:
        - navigate(51.12, 13.13)
        - navigate(, )

    Returns Latitude(0), Longitude(0) if not available.
    """
    selector = response.css("a[onClick*=navigate]")
    lat, lon = 0.0, 0.0
    if selector:
        value = selector.get()
        match = re.match(r".*navigate\((.*)\).*", value)
        if match:
            lat_lon_str = match.groups()[0]
            lat_lon_str = lat_lon_str.replace(" ", "")
            lat_str, lon_str = lat_lon_str.split(",")
            if lat_str:
                lat = float(lat)
            if lon_str:
                lon = float(lon)
    return lat, lon
