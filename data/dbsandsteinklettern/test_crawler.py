import pytest

from data.dbsandsteinklettern import data_crawler
from data.dbsandsteinklettern.data_crawler import create_difficulties_dict as cdd


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
    ],
)
def test_parse_first_ascent(test_input, expected):
    assert data_crawler.parse_first_ascent(test_input) == expected
