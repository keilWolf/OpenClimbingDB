import re

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser
from crawler.climbing_crawler.db_sandstein.saxony_parser import (
    roman_re as roman_re_saxony,
)
from crawler.climbing_crawler.db_sandstein.uiaa_parser import (
    support_re,
    roman_re as roman_re_uiaa,
)

france_re = r"\d[a,b,c]\+?"

regexs = [
    # 6c
    rf"^(?P<rp>{france_re})$",
    # 6c ≙ VIIIa"  ... special sign ... &#8793;combination with saxony
    rf"^(?P<rp>{france_re})≙(?P<saxony>{roman_re_saxony})$",
    # 6a (V A0)
    rf"^(?P<rp>{france_re})\((?P<uiaa>{roman_re_uiaa})(?P<support>{support_re})\)$",
]


def get(match, key):
    if key in match.groupdict() and match.group(key):
        return match.group(key)


class FranceGradeParser(GradeParser):
    def parse(self, content: str):
        """France Grade parsing.

        Examples: 7a, 7a+
        """
        for regex in regexs:
            match = re.match(regex, content)

            if match:
                res = []
                rp = get(match, "rp")
                saxony = get(match, "saxony")
                uiaa = get(match, "uiaa")
                support = get(match, "support")
                if rp:
                    rp = GradeMatch(DiffType.RP, GradeSystem.FRANCE, rp)
                    res.append(rp)
                if saxony:
                    saxony = GradeMatch(DiffType.RP, GradeSystem.SAXON, saxony)
                    res.append(saxony)
                if uiaa and support:
                    diff_type = DiffType[support]
                    g = GradeMatch(diff_type, GradeSystem.UIAA, uiaa)
                    res.append(g)
                return res
