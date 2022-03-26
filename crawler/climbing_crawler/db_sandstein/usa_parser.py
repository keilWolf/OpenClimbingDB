import re

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser

usa_re = r"5\.\d{1,2}[a-d]?"

regexs = [
    # 5.0 5.15d
    rf"^(?P<rp>{usa_re})$",
]


def get(match, key):
    if key in match.groupdict() and match.group(key):
        return match.group(key)


class UsaGradeParser(GradeParser):
    def parse(self, content: str):
        """USA Grade parsing.

        Examples: 5.0 ... 5.15d
        """
        for regex in regexs:
            match = re.match(regex, content)

            if match:
                res = []
                rp = get(match, "rp")
                if rp:
                    rp = GradeMatch(DiffType.RP, GradeSystem.USA, rp)
                    res.append(rp)
                return res
