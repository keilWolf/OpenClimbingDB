"""Spider and parsings to crawl data from dbsandsteinklettern."""
import re
import scrapy
from typing import List


def filter_newline(text: str):
    return text.lstrip("\n").strip()


def get_id_from_url(url):
    return re.match(r".*=(\d+)", url)[1]


def parse_summit_coordinates(string: str):
    re_coordinates = r"(\d{1,}.\d{1,})"
    matches = re.findall(re_coordinates, string)
    if len(matches) < 2:
        raise Exception(f"There should be coordinates for the string {string}")
    lat = float(matches[0])
    lon = float(matches[1])
    return lat, lon


def parse_route_name(line: str):
    groups = re.match(r"(\d?\.?\d?) ?(\*?.*)", line).groups()
    route_id = groups[0]
    route_name = groups[1]
    route_name_alt = ""
    if "/" in route_name:
        route_name, route_name_alt = route_name.split("/")
    route_rating = route_name.count("*")
    route_name = route_name[route_rating:]
    return route_id, route_name, route_name_alt, route_rating


def parse_ring_counts(selectors: List) -> str:
    possible_matches = list(filter(lambda m: "Ringzahl" in m.get(), selectors))
    if len(possible_matches) == 1:
        match = possible_matches[0]
        selectors.remove(match)
        return match.get().split(":")[1].strip()
    else:
        return ""


def parse_climbing_styles(selectors: List) -> List:
    possible_matches = list(filter(lambda m: "Kletterei" in m.get(), selectors))
    if len(possible_matches) == 1:
        match = possible_matches[0]
        selectors.remove(match)
        parts = match.get().split(":")[1].split(",")
        return [p.strip() for p in parts]
    else:
        return []


def create_difficulties_dict(
    af, rp=None, oU=None, jump=None, is_danger=False, is_anstr=False
):
    return {
        "jump": jump,
        "af": af,
        "oU": oU,
        "RP": rp,
        "danger": is_danger,
        "anstr": is_anstr,
    }


def parse_difficulties(content: str):
    """Split difficulties.

    Examples:
        IV
        IV (VI)
        2/Xa RP Xb
        IXb RP IXc
        IXa
        IXc (Xa) RP Xb
        VIIIa RP VIIIb
        V
        V !
        I (II) anstr.
    """
    pattern = r"(\d)?\/?(\w*)( \((.*)\))?( RP (\w*))?( !)?( anstr\.)?"

    match = re.match(pattern, content)
    if match:
        groups = match.groups()
        jump = groups[0]
        af = groups[1]
        oU = groups[3]
        rp = groups[5]
        danger = True if groups[6] else False
        anstr = True if groups[7] else False
        return create_difficulties_dict(af, rp, oU, jump, danger, anstr)

    return {}


def parse_first_ascent(content: str):
    re_date = r".*(\d{2}\.\d{2}\.\d{4})"
    match = re.match(re_date, content)
    fa = {"persons": [], "date": None}
    ascentionists = content
    if match:
        date = match.groups()[0]
        fa["date"] = date
        ascentionists = content.replace(date, "")

    ascentionists = (
        ascentionists.strip()
        .replace(", ", ",")
        .replace(".", ". ")
        .replace("  ", " ")
        .split(",")
    )
    ascentionists = filter(lambda a: len(a) != 0, ascentionists)
    ascentionists = filter(lambda a: a[0].isupper(), ascentionists)
    for asc in ascentionists:
        parts = asc.split(" ")
        if len(parts) == 0:
            raise Exception(f"Something went wrong for {content}")
        elif len(parts) == 1:
            fa["persons"].append({"name": "", "last_name": parts[0]})
        else:
            fa["persons"].append(
                {"name": " ".join(parts[0:-1]), "last_name": parts[-1]}
            )
    return fa


class DBSandsteinSpider(scrapy.Spider):
    name = "db_sandstein"
    start_urls = ["http://db-sandsteinklettern.gipfelbuch.de/adr.php"]

    def __init__(self, *args, **kwargs):
        super(DBSandsteinSpider, self).__init__(*args, **kwargs)
        self.filter = kwargs.get("filter")

    def parse(self, response):
        if self.filter is None:
            countries = response.css('a[href*="boehmen.php"]')
            for country in countries:
                yield response.follow(country, self.parse_area)
        else:
            country = response.css(f'a[href*="boehmen.php"]:contains({self.filter})')
            if len(country) == 0:
                print(f"Not found by filter [{self.filter}].")
                return
            yield response.follow(country[0], self.parse_country)

    def parse_country(self, response):
        country = re.match(r".*land=(.*)", response.url)[1]
        areas = response.css('a[href*="gebiet.php"]')
        for area in areas:
            sub_area_name = area.css("a ::text").get()
            sub_area_id = get_id_from_url(area.css("a").get())
            yield {
                "country": country,
                "area": sub_area_name,
                "area_id": sub_area_id,
            }
            yield response.follow(area, self.parse_area)

    def parse_area(self, response):
        area_id = get_id_from_url(response.url)
        sector_ids = set(re.findall(r'sektorid=(\d+)"', str(response.body)))
        for sector_id in sector_ids:
            sector_ahrefs = response.css(r'a[href*="sektorid\=' + f'{sector_id}"]')
            id_rel_to_area = filter_newline(sector_ahrefs[0].css("::text").get())
            sector_name = filter_newline(sector_ahrefs[1].css("::text").get())
            yield {
                "area_id": area_id,
                "sector": sector_name,
                "db_id": sector_id,
                "id_rel_to_area": id_rel_to_area,
            }
            yield response.follow(sector_ahrefs[0], self.parse_sector)

    def parse_sector(self, response):
        fonts = response.css("font::text").getall()
        filtered_fonts = list(filter(lambda txt: "Alternativ" in txt, fonts))
        alt = ""
        if len(filtered_fonts) == 1:
            alt = filtered_fonts[0].split(":")[1].strip()
        sector_id = get_id_from_url(response.url)
        rows = response.css("tr")
        for row in rows:
            summit_link = row.css('a[href*="weg.php"]')
            summit_name = summit_link.css("::text").get()
            if summit_name is not None:
                db_id = get_id_from_url(summit_link.get())
                summit_id = row.css("font::text").get()
                yield {
                    "sector_id": sector_id,
                    "summit": summit_name,
                    "id_rel_to_sector": summit_id,
                    "db_id": db_id,
                    "sector_alt": alt,
                }
                yield response.follow(summit_link[0], self.parse_summit)

    def parse_summit(self, response):
        header = response.css("h2").css("*:not(font):not(a)::text")
        summit_db_id = get_id_from_url(response.url)
        summit_rel_id = header[0].get().strip()
        summit_name = header[1].get().strip()
        summit_name_alt = header[2].get().replace("/", "").strip()
        text_coordinates = response.css(
            'font[size="-1"]:contains(Gipfelkoordinaten)::text'
        ).get()
        if text_coordinates is not None:
            lat, lon = parse_summit_coordinates(text_coordinates)
        else:
            lat = 0
            lon = 0

        yield {
            "summit_db_id": summit_db_id,
            "summit_rel_id": summit_rel_id,
            "summit_name": summit_name,
            "summit_name_alt": summit_name_alt,
            "lat": lat,
            "lon": lon,
        }

        route_links = response.css('a[href*="komment.php"]')
        for route_link in route_links:
            yield response.follow(route_link, self.parse_route)

    def parse_route(self, response):
        summit_id = get_id_from_url(response.css("b a").get())
        summit_name = response.css("b a::text").get().replace("\n", "").strip()
        summit_name_alt = ""
        if "/" in summit_name:
            splits = summit_name.split("/")
            summit_name = splits[0].strip()
            summit_name_alt = splits[1].strip()

        route_id, route_name, route_name_alt, route_rating = parse_route_name(
            response.css("b::text")[1].get().replace("\n", "").strip()
        )

        txts = response.css(":not(a)::text")
        f_txts = list(
            filter(lambda msg: msg.get() != "\n" and msg.get() != "\n\t", txts)
        )
        eo = next(filter(lambda m: "Angaben zum Weg" in m.get(), f_txts))
        end_index = f_txts.index(eo)
        bo = next(filter(lambda m: route_name in m.get(), f_txts))
        start_index = f_txts.index(bo) + 1
        f_txts = f_txts[start_index:end_index]

        ring_count = parse_ring_counts(f_txts)
        climbing_styles = parse_climbing_styles(f_txts)
        difficulties = parse_difficulties(
            f_txts[0].get().replace("\n", "").replace("*", "")
        )
        first_ascent = parse_first_ascent(f_txts[1].get().replace("\n", ""))

        yield {
            "summit_id": summit_id,
            "summit_name": summit_name,
            "summit_name_alt": summit_name_alt,
            "route_id": route_id,
            "route_name": route_name,
            "route_name_alt": route_name_alt,
            "route_rating": route_rating,
            "ring_count": ring_count,
            "climbing_styles": climbing_styles,
            "difficulties": difficulties,
            "first_ascent": first_ascent,
        }
