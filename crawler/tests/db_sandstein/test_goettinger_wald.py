from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


def test_parse_goettinger_wald_special_case():
    res = GradeParser().parse("3h")
    assert len(res) == 1
    grade_match = res[0]
    assert grade_match.diff_type == DiffType.JUMP
    assert grade_match.gs == GradeSystem.SAXON_JUMP
    assert grade_match.grade_str == "3"
