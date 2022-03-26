import re

from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.saxony_parser import (
    roman_re as roman_re_saxony,
)
from crawler.climbing_crawler.db_sandstein.uiaa_parser import (
    arabic_re as arabic_re_uiaa,
)
from crawler.climbing_crawler.db_sandstein.uiaa_parser import roman_re as roman_re_uiaa
from crawler.climbing_crawler.db_sandstein.uiaa_parser import (
    roman_to_arabic,
    support_re,
)

france_re = r"\d[a,b,c]\+?"

regexs = [
    # 6c
    rf"^(?P<rp>{france_re})$",
    # 6c ≙ VIIIa"  ... special sign ... &#8793;combination with saxony
    rf"^(?P<rp>{france_re})≙(?P<saxony>{roman_re_saxony})$",
    # 6a (V A0)
    rf"^(?P<rp>{france_re})\((?P<uiaa>{roman_re_uiaa})(?P<support>{support_re})\)$",
    # 6c+/7a
    rf"^(?P<af>{france_re})\/(?P<rp>{france_re})$",
    # 6 (6b+)
    rf"^(?P<rp_uiaa>{arabic_re_uiaa})\((?P<rp>{france_re})\)$",
    # 7 / 6b
    rf"^(?P<rp_uiaa>{arabic_re_uiaa})\/(?P<rp>{france_re})$",
]


def get(match, key):
    if key in match.groupdict() and match.group(key):
        return match.group(key)


class FranceGradeParser(GradeParser):
    def parse(self, content: str):
        """France Grade parsing.

        Examples: 7a, 7a+
        """
        grade_str = content
        for regex in regexs:
            match = re.match(regex, grade_str)

            if match:
                res = []
                af = get(match, "af")
                rp = get(match, "rp")
                saxony = get(match, "saxony")
                uiaa = get(match, "uiaa")
                rp_uiaa_arabic = get(match, "rp_uiaa")
                support = get(match, "support")
                if af:
                    res.append(GradeMatch(DiffType.AF, GradeSystem.FRANCE, af))
                if rp:
                    res.append(GradeMatch(DiffType.RP, GradeSystem.FRANCE, rp))
                if rp_uiaa_arabic:
                    res.append(
                        GradeMatch(DiffType.RP, GradeSystem.UIAA, rp_uiaa_arabic)
                    )
                if saxony:
                    saxony = GradeMatch(DiffType.RP, GradeSystem.SAXON, saxony)
                    res.append(saxony)
                if uiaa and support:
                    uiaa_arabic = roman_to_arabic(uiaa)
                    diff_type = DiffType[support]
                    g = GradeMatch(diff_type, GradeSystem.UIAA, uiaa_arabic)
                    res.append(g)
                return res
