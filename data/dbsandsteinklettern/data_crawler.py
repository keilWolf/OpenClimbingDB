import asyncio
import aiohttp
import tqdm
import json
import re
from bs4 import BeautifulSoup

gipfel_base_path = "http://db-sandsteinklettern.gipfelbuch.de/weg.php?gipfelid={}"
route_base_path = "http://db-sandsteinklettern.gipfelbuch.de/komment.php?wegid={}"

# https://compiletoi.net/fast-scraping-in-python-with-asyncio/

OUT = "./crawled.jsonl"


async def request_route(id):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(route_base_path.format(id), compress=True) as resp:
                content = await resp.read()
                data = await parse_route(content)
                with open(OUT, "a") as f:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")


async def parse_route(content: str):
    infos = {}

    soup = BeautifulSoup(content, "lxml")

    links = soup.find_all("a")

    summit_tag_list = list(filter(lambda x: "weg.php?gipfelid" in str(x), links))
    if len(summit_tag_list) == 0:
        raise ValueError("Here is nothing")

    summit_tag = summit_tag_list[0]
    summit_id = summit_tag.attrs["href"].split("=")[1]

    infos["area"] = next(filter(lambda x: "gebiet" in str(x), links)).text
    infos["sector"] = next(filter(lambda x: "sektor" in str(x), links)).text
    infos["summit_name"] = summit_tag.text
    infos["summit_id"] = str(await request_summit_id(summit_id))

    route_name_tag = summit_tag.next_element.next_element.next_element
    route_name = re.match(r"\d?(\*?.*)", route_name_tag.strip("\n")).groups()[0]
    infos["route_name"] = route_name

    diff_tag = route_name_tag.find_next("a").next_element.next_element
    infos["diff"] = diff_tag

    first_ascent = diff_tag.find_next("a").next_element.next_element
    infos["first_ascent"] = first_ascent

    route_descr = (
        first_ascent.find_next("a").find_next("a").previous_element.previous_element
    )

    if route_descr.startswith("Kletterei"):
        route_descr = (
            route_descr.find_next("a").find_next("a").previous_element.previous_element
        )

    infos["descr"] = route_descr

    for info_key in infos:
        infos[info_key] = infos[info_key].strip("\n").strip()

    infos["diff"] = parse_difficulties(infos["diff"])
    infos["first_ascent"] = parse_first_ascent(infos["first_ascent"])
    infos["route_name"] = parse_route_name(infos["route_name"])

    return infos


async def request_summit_id(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(gipfel_base_path.format(id), compress=True) as resp:
            content = await resp.read()
            return parse_summit_id(content)


def parse_summit_id(content: str):
    soup = BeautifulSoup(content, "lxml")

    h2_tags = soup.find_all("h2")

    g_id = str(h2_tags[0].next_element).strip()
    g_id = int(g_id)

    return g_id


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
        ascentionists.strip().replace(", ", ",").replace(".", ". ").split(",")
    )
    ascentionists = filter(lambda a: len(a) != 0, ascentionists)
    ascentionists = filter(lambda a: a[0].isupper(), ascentionists)
    for asc in ascentionists:
        parts = asc.split(" ")
        if len(parts) == 1:
            fa["persons"].append({"name": "", "last_name": parts[0]})
        elif len(parts) == 2:
            fa["persons"].append({"name": parts[0], "last_name": parts[1]})
        else:
            raise Exception(f"Something went wrong for {content}")
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
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(50)
    loop.run_until_complete(wait_with_progress([request_route(i) for i in range(1000)]))
