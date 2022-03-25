import re

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser
from crawler.climbing_crawler.db_sandstein.saxony_parser import roman_re

france_re = r"\d[a,b,c]\+?"

regexs = [
    # 6c
    rf"^(?P<rp>{france_re})$",
    # 6c ≙ VIIIa"  ... special sign ... &#8793;combination with saxony
    rf"^(?P<rp>{france_re})≙(?P<saxony>{roman_re})$",
]


class FranceGradeParser(GradeParser):
    def parse(self, content: str):
        """France Grade parsing.

        Examples: 7a, 7a+
        """
        for regex in regexs:
            match = re.match(regex, content)

            if match:
                res = []
                if "rp" in match.groupdict() and match.group("rp"):
                    rp = GradeMatch(DiffType.RP, GradeSystem.FRANCE, match.group("rp"))
                    res.append(rp)
                if "saxony" in match.groupdict() and match.group("saxony"):
                    saxony = GradeMatch(
                        DiffType.RP, GradeSystem.SAXON, match.group("saxony")
                    )
                    res.append(saxony)
                return res
