import pytest

from crawler.climbing_crawler.db_sandstein_util import parse_difficulties
from crawler.climbing_crawler.db_sandstein_util import create_difficulties_dict as cdd


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
        ("Sprung 2 od. II", cdd("II", jump="2")),
        ("7a", cdd("VIIa", rp="VIIa")),
    ],
)
def test_parse_difficulties(test_input, expected):
    assert parse_difficulties(test_input) == expected
