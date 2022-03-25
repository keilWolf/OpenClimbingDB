import pytest

from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "8a+",
            [
                ["8a+", DiffType.AF],
            ],
        ),
        (
            "8a",
            [
                ["8a", DiffType.AF],
            ],
        ),
    ],
)
def test_parse_france(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type = expected[i]
        assert grade_match.diff_type == diff_type
        assert grade_match.grade_str == grade_str
        assert grade_match.gs == GradeSystem.FRANCE
