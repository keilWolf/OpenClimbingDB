import pytest

from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem

from crawler.climbing_crawler.db_sandstein.uiaa_parser import fix_sign_for_low_grades


def test_fix_sign():
    assert fix_sign_for_low_grades("4+") == "4"
    assert fix_sign_for_low_grades("2-") == "2"
    assert fix_sign_for_low_grades("5+") == "5+"
    assert fix_sign_for_low_grades("5") == "5"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "3+",
            [
                ["3", DiffType.RP],
            ],
        ),
        (
            "7",
            [
                ["7", DiffType.RP],
            ],
        ),
        (
            "5+ A1",
            [
                ["5+", DiffType.A1],
            ],
        ),
        (
            "5+ A1 (6+)",
            [
                ["6+", DiffType.RP],
                ["5+", DiffType.A1],
            ],
        ),
        (
            "6+/A3",
            [
                ["6+", DiffType.A3],
            ],
        ),
        (
            "5+ (5-A0)",
            [
                ["5+", DiffType.RP],
                ["5-", DiffType.A0],
            ],
        ),
        (
            "8+(6-/A1)",
            [
                ["8+", DiffType.RP],
                ["6-", DiffType.A1],
            ],
        ),
        (
            "3+ / 4+",
            [
                ["4", DiffType.RP],
                ["3", DiffType.AF],
            ],
        ),
        (
            "7+ (original 8)",
            [
                ["7+", DiffType.RP],
            ],
        ),
        (
            "3, meist 2",
            [
                ["3", DiffType.RP],
            ],
        ),
        (
            "3+",
            [
                ["3", DiffType.RP],
            ],
        ),
        (
            "1-",
            [
                ["1", DiffType.RP],
            ],
        ),
        (
            "4-",
            [
                ["4", DiffType.RP],
            ],
        ),
        (
            "1-2",
            [
                ["2", DiffType.RP],
                ["1", DiffType.AF],
            ],
        ),
        (
            "2 (5)",
            [
                ["5", DiffType.RP],
                ["2", DiffType.AF],
            ],
        ),
        (
            "3+ (6+)",
            [
                ["6+", DiffType.RP],
                ["3", DiffType.AF],
            ],
        ),
    ],
)
def test_parse_uiaa_arabic(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type = expected[i]
        assert grade_match.gs == GradeSystem.UIAA
        assert grade_match.diff_type == diff_type
        assert grade_match.grade_str == grade_str


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "IV",
            [
                ["4", DiffType.RP],
            ],
        ),
        (
            "V-",
            [
                ["5-", DiffType.RP],
            ],
        ),
        (
            "X+",
            [
                ["10+", DiffType.RP],
            ],
        ),
        (
            "II-V",
            [
                ["5", DiffType.RP],
                ["2", DiffType.AF],
            ],
        ),
        (
            "III-",
            [
                ["3", DiffType.RP],
            ],
        ),
        (
            "III+",
            [
                ["3", DiffType.RP],
            ],
        ),
        (
            "IV-",
            [
                ["4", DiffType.RP],
            ],
        ),
    ],
)
def test_parse_uiaa_roman(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type = expected[i]
        assert grade_match.gs == GradeSystem.UIAA
        assert grade_match.grade_str == grade_str
        assert grade_match.diff_type == diff_type
