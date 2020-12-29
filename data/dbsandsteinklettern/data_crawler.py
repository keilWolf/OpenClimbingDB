import traceback
import asyncio
import aiohttp
import tqdm
import json
import re
from bs4 import BeautifulSoup

gipfel_base_path = "http://db-sandsteinklettern.gipfelbuch.de/weg.php?gipfelid={}"
route_base_path = "http://db-sandsteinklettern.gipfelbuch.de/komment.php?wegid={}"


async def request_route(id):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(route_base_path.format(id), compress=True) as resp:
                content = await resp.read()
                try:
                    data = await parse_route(content)
                    with open(OUT, "a") as f:
                        f.write(json.dumps(data, ensure_ascii=False) + "\n")
                except ValueError:
                    # Go to next element. Side is empty.
                    pass
                except Exception:
                    print(traceback.format_exc())
                    print(f"Something went wrong for content \n {content}")


async def parse_route(content: str):
    infos = {}

    soup = BeautifulSoup(content, "lxml")

    links = soup.find_all("a")

    summit_tag_list = list(filter(lambda x: "weg.php?gipfelid" in str(x), links))
    summit_tag = summit_tag_list[0]
    summit_id = summit_tag.attrs["href"].split("=")[1]
    if summit_id == "":
        raise ValueError("Here is nothing")

    infos["area"] = next(filter(lambda x: "gebiet" in str(x), links)).text
    infos["sector"] = next(filter(lambda x: "sektor" in str(x), links)).text
    infos["summit_name"] = summit_tag.text
    infos["summit_infos"] = await request_summit_id(summit_id)
    infos["summit_infos"]["db_id"] = summit_id

    route_name_tag = summit_tag.next_element.next_element.next_element
    route_name = get_route_name(route_name_tag.strip("\n"))
    infos["route_name"] = parse_route_name(route_name)

    diff_tag = route_name_tag.find_next("a").next_element.next_element
    infos["diff"] = parse_difficulties(diff_tag.strip("\n").strip())

    first_ascent = diff_tag.find_next("a").next_element.next_element
    infos["first_ascent"] = parse_first_ascent(first_ascent.strip("\n").strip())

    infos["descr"] = get_route_description(first_ascent.find_next("a"))

    return infos


def get_route_name(line: str):
    return re.match(r"\d?\.?\d? ?(\*?.*)", line).groups()[0]


def get_route_description(content):
    route_descr = content.find_next("a").previous_element.previous_element

    if route_descr.startswith("Kletterei"):
        route_descr = (
            route_descr.find_next("a").find_next("a").previous_element.previous_element
        )

    return route_descr.strip("\n").strip()


async def request_summit_id(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(gipfel_base_path.format(id), compress=True) as resp:
            content = await resp.read()
            return parse_summit_id(content)


def parse_summit_id(content: str):
    soup = BeautifulSoup(content, "lxml")

    h2_tags = soup.find_all("h2")

    infos = {}
    infos["id_in_sector"] = str(h2_tags[0].next_element).strip()

    # find coordinates
    fonts = soup.findAll("font")
    for font in fonts[:10]:
        text = str(font.next_element).strip()
        if text.startswith("Gipfelkoordinaten"):
            lat, lon = parse_summit_coordinates(text)
            infos["lat"] = lat
            infos["lon"] = lon

    return infos


def parse_summit_coordinates(string: str):
    re_coordinates = r"(\d{1,}.\d{1,})"
    matches = re.findall(re_coordinates, string)
    if len(matches) < 2:
        raise Exception(f"There should be coordinates for the string {string}")
    lat = float(matches[0])
    lon = float(matches[1])
    return lat, lon


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


def create_route_name_dict(name, rating):
    return {"name": name, "rating": rating}


def parse_route_name(route_name):
    if "**" in route_name:
        return create_route_name_dict(route_name.split("**")[1], 2)
    elif "*" in route_name:
        return create_route_name_dict(route_name.split("*")[1], 1)
    else:
        return create_route_name_dict(route_name, 0)


async def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f


if __name__ == "__main__":
    from_num = 100000
    to_num = 110000
    max_num = 105309

    OUT = f"./crawled_{from_num}-{to_num}.jsonl"
    print(f"write output to {OUT}")

    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(100)
    loop.run_until_complete(
        wait_with_progress([request_route(i) for i in range(from_num, to_num)])
    )
