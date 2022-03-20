import pytest

from crawler.climbing_crawler.db_sandstein_util import (
    GradeParser,
    DiffType,
    GradeSystem,
)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "Sprung 2",
            [
                ["2", DiffType.JUMP],
            ],
        ),
        (
            "Sprung 2 od. II",
            [
                ["2", DiffType.JUMP],
                ["II", DiffType.RP],
            ],
        ),
        (
            "Sprung 3 od. VIIa",
            [
                ["3", DiffType.JUMP],
                ["VIIa", DiffType.RP],
            ],
        ),
        (
            "IV (VI)",
            [
                ["IV", DiffType.A0],
                ["VI", DiffType.RP],
            ],
        ),
        (
            "2/Xa RP Xb",
            [
                ["2", DiffType.JUMP],
                ["Xa", DiffType.AF],
                ["Xb", DiffType.RP],
            ],
        ),
        (
            "IXb RP IXc",
            [
                ["IXb", DiffType.AF],
                ["IXc", DiffType.RP],
            ],
        ),
        (
            "IXa !",
            [
                ["IXa", DiffType.RP],
            ],
        ),
        (
            "VIIIa RP VIIIb !",
            [
                ["VIIIa", DiffType.AF],
                ["VIIIb", DiffType.RP],
            ],
        ),
        (
            "I (II) anstr.",
            [
                ["I", DiffType.A0],
                ["II", DiffType.RP],
            ],
        ),
        (
            "IXc (Xa) RP Xb",
            [
                ["IXc", DiffType.A0],
                ["Xb", DiffType.RP],
                ["Xa", DiffType.AF],
            ],
        ),
        (
            "7a",
            [
                ["VIIa", DiffType.RP],
            ],
        ),
        (
            "VII b",
            [
                ["VIIb", DiffType.RP],
            ],
        ),
        (
            "II/1",
            [
                ["1", DiffType.JUMP],
                ["II", DiffType.RP],
            ],
        ),
        (
            r"VIIc\/RPVIIIa",
            [
                ["VIIc", DiffType.AF],
                ["VIIIa", DiffType.RP],
            ],
        ),
        (
            "VIIb-c",
            [
                ["VIIb", DiffType.AF],
                ["VIIc", DiffType.RP],
            ],
        ),
        (
            "V-VIIb",
            [
                ["V", DiffType.AF],
                ["VIIb", DiffType.RP],
            ],
        ),
        (
            "1/I",
            [
                ["1", DiffType.JUMP],
                ["I", DiffType.RP],
            ],
        ),
        (
            "*V",
            [
                ["V", DiffType.RP],
            ],
        ),
        (
            "VIIc/RPVIIIa",
            [
                ["VIIc", DiffType.AF],
                ["VIIIa", DiffType.RP],
            ],
        ),
        (
            "III/VIIb",
            [
                ["III", DiffType.AF],
                ["VIIb", DiffType.RP],
            ],
        ),
    ],
)
def test_parse_saxony_grades(test_input, expected):
    res = GradeParser.saxony().parse(test_input)
    assert len(res) == len(expected)
    for grade_match in res:
        assert grade_match.gs == GradeSystem.SAXON
        assert [grade_match.grade_str, grade_match.diff_type] in expected


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


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "3+",
            [
                ["3+", DiffType.RP],
            ],
        ),
        (
            "7",
            [
                ["7", DiffType.RP],
            ],
        ),
        (
            "5+ A1 (6+)",
            [
                ["5+", DiffType.A1],
                ["6+", DiffType.RP],
            ],
        ),
        (
            "6+/A3",
            [
                ["?", DiffType.A3],
                ["6+", DiffType.RP],
            ],
        ),
        (
            "5+ (5-A0)",
            [
                ["5-", DiffType.A0],
                ["5+", DiffType.RP],
            ],
        ),
        (
            "8+(6-/A1)",
            [
                ["6-", DiffType.A1],
                ["8+", DiffType.RP],
            ],
        ),
        (
            "3+ / 4+",
            [
                ["3+", DiffType.AF],
                ["4+", DiffType.RP],
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
    ],
)
def test_parse_uiaa_arabic(test_input, expected):
    res = GradeParser().parse(test_input)
    assert len(res) == len(expected)
    for i, grade_match in enumerate(res):
        grade_str, diff_type = expected[i]
        assert grade_match.gs == GradeSystem.UIAA
        assert [grade_str, diff_type] in expected
        # assert grade_match.diff_type == diff_type
        # assert grade_match.grade_str == grade_str


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
                ["2", DiffType.AF],
                ["5", DiffType.RP],
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
        assert [grade_str, diff_type] in expected


"""
Jordanien
- T.D. Sup.
- E.D. A2
- E.D.Sup.
- ABO
- T.D. Sup.(E.D. Inf.)
- E.D. Inf.(E.D. Sup.)
- T.D.
- A.D.Sup
"""


def test_parse_jordan():
    pass
