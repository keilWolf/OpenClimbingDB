import pytest

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.parser import GradeParser


@pytest.mark.parametrize(
    "test_input, expected",
    [
        # http://db-sandsteinklettern.gipfelbuch.de/komment.php?wegid=106584
        (
            "2h",
            [
                ["2", DiffType.JUMP, GradeSystem.SAXON_JUMP],
            ],
        ),
        # http://db-sandsteinklettern.gipfelbuch.de/komment.php?wegid=106583
        (
            "2-h",
            [
                ["2", DiffType.JUMP, GradeSystem.SAXON_JUMP],
            ],
        ),
    ],
)
def test_parse_france(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type, gs = expected[i]
        assert grade_match.diff_type == diff_type
        assert grade_match.grade_str == grade_str
        assert grade_match.gs == gs


def test_parse_zero_init():
    res = GradeParser().parse("0")
    assert len(res) == 0
