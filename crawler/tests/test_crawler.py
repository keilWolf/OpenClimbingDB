import pytest

from climbing_crawler.spiders import db_sandstein_spider as data_crawler
from climbing_crawler.spiders.db_sandstein_spider import (
    create_difficulties_dict as cdd,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("IV", cdd("IV")),
        ("IV (VI)", cdd("IV", oU="VI")),
        ("2/Xa RP Xb", cdd("Xa", rp="Xb", jump="2")),
        ("IXb RP IXc", cdd("IXb", rp="IXc")),
        ("IXa !", cdd("IXa", is_danger=True)),
        ("VIIIa RP VIIIb !", cdd("VIIIa", rp="VIIIb", is_danger=True)),
        ("I (II) anstr.", cdd("I", oU="II", is_anstr=True)),
        ("IXc (Xa) RP Xb", cdd("IXc", oU="Xa", rp="Xb")),
    ],
)
def test_parse_difficulties(test_input, expected):
    assert data_crawler.parse_difficulties(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Alter Weg", {"name": "Alter Weg", "rating": 0}),
        ("*Alter Weg", {"name": "Alter Weg", "rating": 1}),
        ("**Alter Weg", {"name": "Alter Weg", "rating": 2}),
    ],
)
def test_route_name_without_star(test_input, expected):
    assert data_crawler.parse_route_name(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "Friedrich Brosin, H.Wenzel, R.Püschner, F.Gerbing 21.07.1899",
            {
                "persons": [
                    {"name": "Friedrich", "last_name": "Brosin"},
                    {"name": "H.", "last_name": "Wenzel"},
                    {"name": "R.", "last_name": "Püschner"},
                    {"name": "F.", "last_name": "Gerbing"},
                ],
                "date": "21.07.1899",
            },
        ),
        (
            "Friedrich Brosin, H.Wenzel",
            {
                "persons": [
                    {"name": "Friedrich", "last_name": "Brosin"},
                    {"name": "H.", "last_name": "Wenzel"},
                ],
                "date": None,
            },
        ),
        (
            "Kurt Steinbach, 11.06.1919",
            {
                "persons": [
                    {"name": "Kurt", "last_name": "Steinbach"},
                ],
                "date": "11.06.1919",
            },
        ),
        (
            "Carl Rau, vor 1914 01.01.1914",
            {
                "persons": [
                    {"name": "Carl", "last_name": "Rau"},
                ],
                "date": "01.01.1914",
            },
        ),
        (
            "Polesný, und Gef. 21.06.1985",
            {
                "persons": [
                    {"name": "", "last_name": "Polesný"},
                ],
                "date": "21.06.1985",
            },
        ),
        (
            "Stanislav Lukavský, J. Polák 12.06.1977",
            {
                "persons": [
                    {"name": "Stanislav", "last_name": "Lukavský"},
                    {"name": "J.", "last_name": "Polák"},
                ],
                "date": "12.06.1977",
            },
        ),
        (
            "H.L. Stutte 10.04.1981",
            {
                "persons": [
                    {"name": "H. L.", "last_name": "Stutte"},
                ],
                "date": "10.04.1981",
            },
        ),
    ],
)
def test_parse_first_ascent(test_input, expected):
    assert data_crawler.parse_first_ascent(test_input) == expected


def test_parse_summit_coordinates():
    test_input = """Gipfelkoordinaten: 50.615310 Grad nördlicher Breite \n  und 16.120550 Grad östlicher Länge [N50°36\'55.1"\n  O16°7\'13.9"]"""  # noqa: E501
    lat, lon = data_crawler.parse_summit_coordinates(test_input)
    assert lat == 50.615310
    assert lon == 16.120550


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Talseite", "Talseite"),
        ("1 Talseite", "Talseite"),
        ("1. Talseite", "Talseite"),
        ("6.2 Talseite direkt", "Talseite direkt"),
        ("6.2 **Talseite direkt", "**Talseite direkt"),
    ],
)
def test_get_route_name(test_input, expected):
    assert data_crawler.get_route_name(test_input) == expected
