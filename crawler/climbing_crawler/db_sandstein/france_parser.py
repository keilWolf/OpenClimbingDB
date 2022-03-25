import re

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser


class FranceGradeParser(GradeParser):
    def parse(self, content: str):
        """France Grade parsing.

        Examples: 7a, 7a+
        """
        pattern = r"^\d[a,b,c]\+?$"
        match = re.match(pattern, content)
        if match:
            return [
                GradeMatch(DiffType.AF, GradeSystem.FRANCE, match.string),
            ]
