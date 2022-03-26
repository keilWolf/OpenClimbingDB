import pytest

from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "5.0",
            [
                ["5.0", DiffType.RP],
            ],
        ),
        (
            "5.6",
            [
                ["5.6", DiffType.RP],
            ],
        ),
        (
            "5.11b",
            [
                ["5.11b", DiffType.RP],
            ],
        ),
        (
            "5.15d",
            [
                ["5.15d", DiffType.RP],
            ],
        ),
    ],
)
def test_parse_usa(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type = expected[i]
        assert grade_match.gs == GradeSystem.USA
        assert grade_match.grade_str == grade_str
        assert grade_match.diff_type == diff_type
