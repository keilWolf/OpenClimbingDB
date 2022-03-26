import pytest
from crawler.climbing_crawler.db_sandstein.parser import GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


@pytest.mark.parametrize("test_input", ["12", "20", "38"])
def test_parse_france(test_input):
    res = GradeParser().parse(test_input)
    assert len(res) == 1
    grade_match = res[0]
    assert grade_match.diff_type == DiffType.RP
    assert grade_match.gs == GradeSystem.EWBANK_SOUTH_AFRICA
    assert grade_match.grade_str == test_input


@pytest.mark.parametrize("test_input", ["0", "39"])
def test_out_of_range(test_input):
    with pytest.raises(ValueError):
        GradeParser().parse(test_input)
