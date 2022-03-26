from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


def test_parse_goettinger_wald():
    res = GradeParser().parse("3h")
    assert len(res) == 1
    grade_match = res[0]
    assert grade_match.diff_type == DiffType.JUMP
    assert grade_match.gs == GradeSystem.SAXON_JUMP
    assert grade_match.grade_str == "3"


def test_parse_zero_init():
    res = GradeParser().parse("0")
    assert len(res) == 0
