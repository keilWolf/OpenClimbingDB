import pytest

from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            "PP VIIIb",
            [
                ["VIIIb", DiffType.RP, GradeSystem.SAXON],
            ],
        ),
        (
            "Ii-III",
            [
                ["II", DiffType.AF, GradeSystem.SAXON],
                ["III", DiffType.RP, GradeSystem.SAXON],
            ],
        ),
        (
            "VIIc RP VIII",
            [
                ["VIIc", DiffType.AF, GradeSystem.SAXON],
                ["VIIIa", DiffType.RP, GradeSystem.SAXON],
            ],
        ),
        (
            "VIIB",
            [
                ["VIIb", DiffType.RP, GradeSystem.SAXON],
            ],
        ),
    ],
)
def test_parse_saxony_grades_with_spelling_error(test_input, expected):
    res = GradeParser.saxony().parse(test_input)
    assert len(res) == len(expected)
    for grade_match in res:
        assert [
            grade_match.grade_str,
            grade_match.diff_type,
            grade_match.gs,
        ] in expected


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
        (
            "RPVIIIb",
            [
                ["VIIIb", DiffType.RP],
            ],
        ),
        (
            "I oder 1",
            [
                ["1", DiffType.JUMP],
                ["I", DiffType.RP],
            ],
        ),
        (
            "2/II (IV)",
            [
                ["2", DiffType.JUMP],
                ["II", DiffType.A0],
                ["IV", DiffType.RP],
            ],
        ),
        # http://db-sandsteinklettern.gipfelbuch.de/komment.php?wegid=112485
        (
            "IV/A1",
            [
                ["IV", DiffType.A1],
            ],
        ),
    ],
)
def test_parse_saxony_grades(test_input, expected):
    res = GradeParser.saxony().parse(test_input)
    assert len(res) == len(expected)
    for grade_match in res:
        if grade_match.diff_type == DiffType.JUMP:
            assert grade_match.gs == GradeSystem.SAXON_JUMP
        else:
            assert grade_match.gs == GradeSystem.SAXON
        assert [grade_match.grade_str, grade_match.diff_type] in expected
